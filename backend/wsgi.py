"""
WSGI configuration per PythonAnywhere
Questo file permette a PythonAnywhere di eseguire FastAPI
"""
import sys
import os

# Aggiungi path backend al PYTHONPATH
# Sostituisci 'TUO_USERNAME' con il tuo username PythonAnywhere
path = os.path.dirname(os.path.abspath(__file__))
if path not in sys.path:
    sys.path.insert(0, path)

# Imposta working directory
os.chdir(path)

# Importa app FastAPI
try:
    from app.main_simple import app
    # Wrapper WSGI per FastAPI
    application = app
except Exception as e:
    # Fallback in caso di errore
    def application(environ, start_response):
        status = '500 Internal Server Error'
        headers = [('Content-Type', 'text/plain')]
        start_response(status, headers)
        return [f'Error loading app: {str(e)}'.encode()]

