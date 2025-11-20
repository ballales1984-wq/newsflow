"""
WSGI wrapper per FastAPI usando Mangum
PythonAnywhere richiede WSGI, ma FastAPI è ASGI
"""
import sys
import os

path = '/home/braccobaldo/newsflow/backend'
if path not in sys.path:
    sys.path.insert(0, path)

os.chdir(path)

try:
    # Importa Mangum e app FastAPI
    from mangum import Mangum
    from app.main_simple import app
    
    # Crea wrapper WSGI usando Mangum
    mangum_handler = Mangum(app, lifespan="off")
    
    # Wrapper WSGI standard
    def application(environ, start_response):
        """WSGI application wrapper"""
        return mangum_handler(environ, start_response)
    
except Exception as e:
    import traceback
    traceback.print_exc()
    
    def application(environ, start_response):
        status = '500 Internal Server Error'
        headers = [('Content-Type', 'text/plain; charset=utf-8')]
        start_response(status, headers)
        error_msg = f'Error: {str(e)}\nPath: {path}\n'
        return [error_msg.encode('utf-8')]

