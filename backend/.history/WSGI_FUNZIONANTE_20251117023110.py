"""
WSGI configuration FUNZIONANTE per FastAPI su PythonAnywhere
Usa un wrapper personalizzato per convertire WSGI -> ASGI
"""
import sys
import os

path = '/home/braccobaldo/newsflow/backend'
if path not in sys.path:
    sys.path.insert(0, path)

os.chdir(path)

from app.main_simple import app
import asyncio
from io import BytesIO

class WSGI2ASGI:
    """Wrapper che converte WSGI environ in ASGI e chiama app FastAPI"""

    def __init__(self, asgi_app):
        self.asgi_app = asgi_app

    def __call__(self, environ, start_response):
        # Crea o ottieni event loop
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        # Converti WSGI environ in ASGI scope
        scope = {
            'type': 'http',
            'method': environ['REQUEST_METHOD'],
            'path': environ.get('PATH_INFO', '/'),
            'raw_path': environ.get('PATH_INFO', '/').encode(),
            'query_string': environ.get('QUERY_STRING', '').encode(),
            'headers': [
                (k[5:].replace('_', '-').lower().encode(), v.encode())
                for k, v in environ.items()
                if k.startswith('HTTP_')
            ],
            'scheme': environ.get('wsgi.url_scheme', 'http'),
            'server': (environ.get('SERVER_NAME', 'localhost'), int(environ.get('SERVER_PORT', 80))),
            'client': (environ.get('REMOTE_ADDR', '127.0.0.1'), int(environ.get('REMOTE_PORT', 0))),
        }

        # Aggiungi headers standard
        if 'CONTENT_TYPE' in environ:
            scope['headers'].append((b'content-type', environ['CONTENT_TYPE'].encode()))
        if 'CONTENT_LENGTH' in environ:
            scope['headers'].append((b'content-length', environ['CONTENT_LENGTH'].encode()))

        # Message queue per la risposta
        response_status = None
        response_headers = []
        response_body = BytesIO()

        async def receive():
            """Ricevi messaggi HTTP request"""
            body = environ.get('wsgi.input', BytesIO()).read()
            return {
                'type': 'http.request',
                'body': body,
                'more_body': False
            }

        async def send(message):
            """Ricevi messaggi HTTP response"""
            nonlocal response_status, response_headers, response_body

            if message['type'] == 'http.response.start':
                response_status = f"{message['status']} {message.get('reason', 'OK')}"
                response_headers = [(k.decode() if isinstance(k, bytes) else k,
                                    v.decode() if isinstance(v, bytes) else v)
                                   for k, v in message.get('headers', [])]
            elif message['type'] == 'http.response.body':
                body_chunk = message.get('body', b'')
                response_body.write(body_chunk)

        # Esegui app ASGI
        try:
            loop.run_until_complete(self.asgi_app(scope, receive, send))
        except Exception as e:
            import traceback
            error_msg = f"Error: {str(e)}\n{traceback.format_exc()}"
            start_response('500 Internal Server Error',
                         [('Content-Type', 'text/plain; charset=utf-8')])
            return [error_msg.encode('utf-8')]

        # Invia risposta WSGI
        if response_status:
            start_response(response_status, response_headers)
        else:
            start_response('200 OK', [('Content-Type', 'text/html')])

        response_body.seek(0)
        return [response_body.read()]

# Crea application WSGI
application = WSGI2ASGI(app)

