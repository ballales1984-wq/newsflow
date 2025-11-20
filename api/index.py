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

# Variabile globale per catturare errori di inizializzazione
initialization_error = None
handler_mangum = None

try:
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
    print("🔍 DEBUG INIT: Importing mangum...")
    from mangum import Mangum
    print("✅ DEBUG INIT: Mangum imported successfully")

    # STEP 3: Import app FastAPI
    print("🔍 DEBUG INIT: Importing app.main_simple...")
    from app.main_simple import app
    print("✅ DEBUG INIT: app.main_simple imported successfully")

    # STEP 4: Crea handler Mangum
    print("🔍 DEBUG INIT: Creating Mangum handler...")
    handler_mangum = Mangum(app, lifespan="off")
    print("✅ DEBUG INIT: Mangum handler created successfully")

except Exception as e:
    initialization_error = e
    print(f"❌ ERROR during initialization: {str(e)}")
    print(f"❌ ERROR traceback: {traceback.format_exc()}")
    # Non fare raise - lascia che handler gestisca l'errore

# STEP 5: Handler per Vercel
def handler(event, context):
    """Handler per Vercel serverless functions"""
    # Se c'è stato un errore di inizializzazione, restituiscilo
    if initialization_error:
        print(f"❌ HANDLER: Initialization error detected: {initialization_error}")
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "error": "Serverless function initialization failed",
                "message": str(initialization_error),
                "traceback": traceback.format_exc() if os.getenv("VERCEL_ENV") != "production" else None
            })
        }
    
    # Se handler_mangum non è stato creato, restituisci errore
    if handler_mangum is None:
        print(f"❌ HANDLER: handler_mangum is None")
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "error": "Mangum handler not initialized",
                "message": "Handler was not created during initialization"
            })
        }
    
    try:
        print(f"🔍 HANDLER: Received event type={type(event)}")
        if isinstance(event, dict):
            print(f"🔍 HANDLER: Event keys={list(event.keys())}")
            print(f"🔍 HANDLER: Event path={event.get('path', 'N/A')}")
            print(f"🔍 HANDLER: Event method={event.get('httpMethod', 'N/A')}")
        
        # Mangum si aspetta un formato specifico per Vercel
        # Vercel passa eventi in formato AWS Lambda API Gateway
        response = handler_mangum(event, context)
        
        print(f"🔍 HANDLER: Response type={type(response)}")
        
        # Assicurati che la risposta sia nel formato corretto
        if isinstance(response, dict):
            print(f"✅ HANDLER: Response status={response.get('statusCode', 'unknown')}")
            # Se la risposta ha già statusCode, è già nel formato corretto
            if "statusCode" in response:
                return response
            # Altrimenti, potrebbe essere un dict con body/headers
            elif "body" in response or "headers" in response:
                if "statusCode" not in response:
                    response["statusCode"] = 200
                return response
            else:
                # Dict semplice, convertilo in body JSON
                return {
                    "statusCode": 200,
                    "headers": {"Content-Type": "application/json"},
                    "body": json.dumps(response)
                }
        elif isinstance(response, str):
            # Stringa, potrebbe essere già JSON serializzato
            return {
                "statusCode": 200,
                "headers": {"Content-Type": "application/json"},
                "body": response
            }
        else:
            # Altro tipo, serializza come JSON
            return {
                "statusCode": 200,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps(response)
            }
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
