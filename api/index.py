"""
Vercel Serverless Function - ORDINE CORRETTO DI INIZIALIZZAZIONE
1. Setup path e environment
2. Import dipendenze
3. Import app FastAPI
4. Crea handler Mangum
5. Handler per Vercel
"""
import sys
import os
import traceback

# STEP 1: Setup path PRIMA di tutto
current_dir = os.path.dirname(os.path.abspath(__file__))  # api/
project_root = os.path.dirname(current_dir)  # root del progetto
backend_path = os.path.join(project_root, 'backend')

# Aggiungi backend al PYTHONPATH
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

# Imposta working directory
os.chdir(project_root)

# STEP 2: Import dipendenze
try:
    from mangum import Mangum
except ImportError as e:
    print(f"ERROR: Cannot import mangum: {e}")
    raise

# STEP 3: Import app FastAPI
try:
    from app.main_simple import app
except ImportError as e:
    print(f"ERROR: Cannot import app.main_simple: {e}")
    import traceback
    traceback.print_exc()
    raise

# STEP 4: Crea handler Mangum
try:
    handler_mangum = Mangum(app, lifespan="off")
except Exception as e:
    print(f"ERROR: Cannot create Mangum handler: {e}")
    import traceback
    traceback.print_exc()
    raise

# STEP 5: Handler per Vercel
def handler(event, context):
    """Handler per Vercel serverless functions"""
    try:
        # Mangum gestisce automaticamente il formato per Vercel
        response = handler_mangum(event, context)
        return response
    except Exception as e:
        print(f"ERROR in handler: {str(e)}")
        print(f"ERROR traceback: {traceback.format_exc()}")
        import json
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "error": "Serverless function execution failed",
                "message": str(e)
            })
        }
