"""
WSGI wrapper per FastAPI usando Mangum
PythonAnywhere richiede WSGI, ma FastAPI è ASGI
Mangum converte ASGI in WSGI
"""
import sys
import os

# Path backend
path = '/home/braccobaldo/newsflow/backend'
if path not in sys.path:
    sys.path.insert(0, path)

# Imposta working directory
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
    
    print(f"✅ App FastAPI caricata con Mangum da {path}")
    
except Exception as e:
    # Fallback in caso di errore
    print(f"❌ Errore caricamento app: {e}")
    import traceback
    traceback.print_exc()
    
    def application(environ, start_response):
        status = '500 Internal Server Error'
        headers = [('Content-Type', 'text/plain; charset=utf-8')]
        start_response(status, headers)
        error_msg = f'Error loading app: {str(e)}\n\nPath: {path}\n\n'
        return [error_msg.encode('utf-8')]

