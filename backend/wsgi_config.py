"""
Configurazione WSGI per PythonAnywhere
Copia questo contenuto nel file WSGI configuration di PythonAnywhere
"""
import sys
import os

# IMPORTANTE: Sostituisci 'TUO_USERNAME' con il tuo username PythonAnywhere!
# Trova il tuo username nella console: echo $USER
username = 'TUO_USERNAME'  # <-- CAMBIA QUESTO!

# Aggiungi path backend
path = f'/home/{username}/newsflow/backend'
if path not in sys.path:
    sys.path.insert(0, path)

# Imposta working directory
os.chdir(path)

# Importa app FastAPI
try:
    from app.main_simple import app
    # Wrapper WSGI per FastAPI
    application = app
    print(f"✅ App FastAPI caricata da {path}")
except Exception as e:
    # Fallback in caso di errore
    print(f"❌ Errore caricamento app: {e}")
    import traceback
    traceback.print_exc()
    
    def application(environ, start_response):
        status = '500 Internal Server Error'
        headers = [('Content-Type', 'text/plain; charset=utf-8')]
        start_response(status, headers)
        error_msg = f'Error loading app: {str(e)}\n\nPath tried: {path}\n\n'
        return [error_msg.encode('utf-8')]

