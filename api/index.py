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
import json

# STEP 1: Setup path PRIMA di tutto
current_dir = os.path.dirname(os.path.abspath(__file__))  # api/
project_root = os.path.dirname(current_dir)  # root del progetto
backend_path = os.path.join(project_root, 'backend')

print(f"🔍 DEBUG INIT: current_dir={current_dir}")
print(f"🔍 DEBUG INIT: project_root={project_root}")
print(f"🔍 DEBUG INIT: backend_path={backend_path}")
print(f"🔍 DEBUG INIT: cwd={os.getcwd()}")

# Aggiungi backend al PYTHONPATH
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)
    print(f"✅ DEBUG INIT: Added {backend_path} to sys.path")

# Imposta working directory
os.chdir(project_root)
print(f"✅ DEBUG INIT: Changed cwd to {os.getcwd()}")

# Verifica file JSON
json_path_api = os.path.join(project_root, 'api', 'final_news_italian.json')
json_path_backend = os.path.join(project_root, 'backend', 'final_news_italian.json')
digest_path_api = os.path.join(project_root, 'api', 'digest.json')
print(f"🔍 DEBUG INIT: api/final_news exists={os.path.exists(json_path_api)}")
print(f"🔍 DEBUG INIT: backend/final_news exists={os.path.exists(json_path_backend)}")
print(f"🔍 DEBUG INIT: api/digest exists={os.path.exists(digest_path_api)}")
if os.path.exists(json_path_api):
    print(f"🔍 DEBUG INIT: api/final_news size={os.path.getsize(json_path_api)} bytes")
if os.path.exists(json_path_backend):
    print(f"🔍 DEBUG INIT: backend/final_news size={os.path.getsize(json_path_backend)} bytes")

# STEP 2: Import dipendenze
try:
    print("🔍 DEBUG INIT: Importing mangum...")
    from mangum import Mangum
    print("✅ DEBUG INIT: Mangum imported successfully")
except ImportError as e:
    print(f"❌ ERROR: Cannot import mangum: {e}")
    traceback.print_exc()
    raise

# STEP 3: Import app FastAPI
try:
    print("🔍 DEBUG INIT: Importing app.main_simple...")
    from app.main_simple import app
    print("✅ DEBUG INIT: app.main_simple imported successfully")
except ImportError as e:
    print(f"❌ ERROR: Cannot import app.main_simple: {e}")
    traceback.print_exc()
    raise

# STEP 4: Crea handler Mangum
try:
    print("🔍 DEBUG INIT: Creating Mangum handler...")
    handler_mangum = Mangum(app, lifespan="off")
    print("✅ DEBUG INIT: Mangum handler created successfully")
except Exception as e:
    print(f"❌ ERROR: Cannot create Mangum handler: {e}")
    traceback.print_exc()
    raise

# STEP 5: Handler per Vercel
def handler(event, context):
    """Handler per Vercel serverless functions"""
    try:
        print(f"🔍 HANDLER: Received event path={event.get('path', 'unknown')}")
        print(f"🔍 HANDLER: Received event method={event.get('httpMethod', 'unknown')}")
        
        # Mangum gestisce automaticamente il formato per Vercel
        response = handler_mangum(event, context)
        
        print(f"✅ HANDLER: Response status={response.get('statusCode', 'unknown')}")
        return response
    except Exception as e:
        print(f"❌ ERROR in handler: {str(e)}")
        print(f"❌ ERROR traceback: {traceback.format_exc()}")
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "error": "Serverless function execution failed",
                "message": str(e),
                "traceback": traceback.format_exc() if os.getenv("VERCEL_ENV") != "production" else None
            })
        }
