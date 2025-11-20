"""
WSGI configuration CORRETTO per PythonAnywhere
Questo file deve essere copiato nel WSGI configuration file di PythonAnywhere
"""
import sys
import os

# IMPORTANTE: Aggiungi path backend
path = '/home/braccobaldo/newsflow/backend'
if path not in sys.path:
    sys.path.insert(0, path)

# Imposta working directory
os.chdir(path)

try:
    # Verifica che Mangum sia installato
    try:
        from mangum import Mangum
    except ImportError:
        # Se Mangum non è installato, mostra errore chiaro
        raise ImportError("Mangum non installato! Esegui: pip3.10 install --user mangum")
    
    # Importa app FastAPI
    from app.main_simple import app
    
    # Crea wrapper WSGI usando Mangum
    mangum_handler = Mangum(app, lifespan="off")
    
    # Wrapper WSGI standard
    def application(environ, start_response):
        """WSGI application wrapper per FastAPI"""
        return mangum_handler(environ, start_response)
    
except Exception as e:
    import traceback
    error_msg = f"""
    ❌ ERRORE CARICAMENTO APP:
    {str(e)}
    
    Traceback:
    {traceback.format_exc()}
    
    Path tentato: {path}
    """
    print(error_msg)
    
    def application(environ, start_response):
        status = '500 Internal Server Error'
        headers = [('Content-Type', 'text/plain; charset=utf-8')]
        start_response(status, headers)
        return [error_msg.encode('utf-8')]

