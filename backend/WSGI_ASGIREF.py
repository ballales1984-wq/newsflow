"""
WSGI configuration usando asgiref (non Mangum!)
Mangum è per Lambda, asgiref è per WSGI standard
"""
import sys
import os

path = '/home/braccobaldo/newsflow/backend'
if path not in sys.path:
    sys.path.insert(0, path)

os.chdir(path)

from asgiref.wsgi import WsgiToAsgi
from app.main_simple import app

# WsgiToAsgi converte ASGI -> WSGI (inverso di quello che serve)
# In realtà serve ASGI -> WSGI, quindi usiamo un wrapper diverso

# Soluzione: usare asgiref per creare un adapter WSGI
from asgiref.sync import sync_to_async
import asyncio

# Wrapper WSGI per app ASGI
class ASGI2WSGI:
    def __init__(self, asgi_app):
        self.asgi_app = asgi_app
    
    def __call__(self, environ, start_response):
        # Crea un event loop se non esiste
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        # Converti environ WSGI in scope ASGI
        scope = self._wsgi_to_asgi_scope(environ)
        
        # Crea message queue
        messages = []
        
        async def receive():
            return {'type': 'http.request', 'body': environ.get('wsgi.input').read()}
        
        async def send(message):
            messages.append(message)
        
        # Esegui app ASGI
        try:
            loop.run_until_complete(self.asgi_app(scope, receive, send))
        except Exception as e:
            start_response('500 Internal Server Error', [('Content-Type', 'text/plain')])
            return [f'Error: {str(e)}'.encode()]
        
        # Converti messaggi ASGI in risposta WSGI
        status = None
        headers = []
        body = b''
        
        for message in messages:
            if message['type'] == 'http.response.start':
                status = f"{message['status']} {message.get('reason', 'OK')}"
                headers = [(k, v) for k, v in message.get('headers', [])]
            elif message['type'] == 'http.response.body':
                body += message.get('body', b'')
        
        if status:
            start_response(status, headers)
        else:
            start_response('200 OK', [('Content-Type', 'text/html')])
        
        return [body]

    def _wsgi_to_asgi_scope(self, environ):
        """Converti environ WSGI in scope ASGI"""
        return {
            'type': 'http',
            'method': environ['REQUEST_METHOD'],
            'path': environ.get('PATH_INFO', '/'),
            'query_string': environ.get('QUERY_STRING', '').encode(),
            'headers': [
                (k.lower().encode(), v.encode())
                for k, v in environ.items()
                if k.startswith('HTTP_')
            ],
            'scheme': environ.get('wsgi.url_scheme', 'http'),
            'server': (environ.get('SERVER_NAME', ''), int(environ.get('SERVER_PORT', 80))),
            'client': (environ.get('REMOTE_ADDR', ''), int(environ.get('REMOTE_PORT', 0))),
        }

# Crea adapter
application = ASGI2WSGI(app)

