"""
Vercel Serverless Function wrapper per FastAPI backend
Questo file gestisce tutte le routes API come serverless function
"""
import sys
import os
import traceback

try:
    # Aggiungi il path del backend al PYTHONPATH
    # Su Vercel, i file sono nella root del progetto
    current_dir = os.path.dirname(os.path.abspath(__file__))  # api/
    project_root = os.path.dirname(current_dir)  # root del progetto

    # Aggiungi backend al PYTHONPATH
    backend_path = os.path.join(project_root, 'backend')
    if backend_path not in sys.path:
        sys.path.insert(0, backend_path)

    # Imposta il working directory per i file JSON
    # Su Vercel, la root del progetto è dove sono i file JSON
    os.chdir(project_root)

    # Debug: stampa i path (sempre per debugging)
    print(f"DEBUG: current_dir={current_dir}")
    print(f"DEBUG: project_root={project_root}")
    print(f"DEBUG: backend_path={backend_path}")
    print(f"DEBUG: cwd={os.getcwd()}")
    print(f"DEBUG: sys.path={sys.path[:3]}")
    
    # Verifica file JSON (prima in api/, poi in backend/)
    json_path_api = os.path.join(project_root, 'api', 'final_news_italian.json')
    json_path_backend = os.path.join(project_root, 'backend', 'final_news_italian.json')
    print(f"DEBUG: final_news in api/ exists={os.path.exists(json_path_api)}")
    print(f"DEBUG: final_news in backend/ exists={os.path.exists(json_path_backend)}")
    if os.path.exists(json_path_api):
        print(f"DEBUG: final_news in api/ size={os.path.getsize(json_path_api)}")
    if os.path.exists(json_path_backend):
        print(f"DEBUG: final_news in backend/ size={os.path.getsize(json_path_backend)}")

    # Import con gestione errori step-by-step
    print("DEBUG: Step 1 - Importing mangum...")
    try:
        from mangum import Mangum
        print("DEBUG: ✅ Mangum imported successfully")
    except Exception as e:
        print(f"DEBUG: ❌ Error importing mangum: {e}")
        raise
    
    print("DEBUG: Step 2 - Importing app.main_simple...")
    try:
        from app.main_simple import app
        print("DEBUG: ✅ app.main_simple imported successfully")
        print(f"DEBUG: App type: {type(app)}")
    except Exception as e:
        print(f"DEBUG: ❌ Error importing app.main_simple: {e}")
        import traceback
        print(f"DEBUG: Traceback: {traceback.format_exc()}")
        raise

    print("DEBUG: Step 3 - Creating Mangum handler...")
    try:
        mangum_handler = Mangum(app, lifespan="off")
        print("DEBUG: ✅ Mangum handler created successfully")
        initialization_error = None
    except Exception as e:
        print(f"DEBUG: ❌ Error creating Mangum handler: {e}")
        raise

except Exception as e:
    initialization_error = e
    print(f"ERROR during initialization: {str(e)}")
    print(f"ERROR traceback: {traceback.format_exc()}")
    import json
    # Crea un handler di fallback che restituisce informazioni utili
    def error_handler(event, context):
        import json
        error_info = {
            "error": "Serverless function initialization failed",
            "message": str(initialization_error),
            "path": event.get("path", "unknown") if event else "no event",
            "method": event.get("httpMethod", "unknown") if event else "no event"
        }
        # Includi traceback solo in debug
        if os.getenv("VERCEL_ENV") != "production":
            error_info["traceback"] = traceback.format_exc()
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(error_info)
        }
    mangum_handler = error_handler

def handler(event, context):
    """Handler per Vercel serverless functions"""
    try:
        # Mangum restituisce direttamente il formato corretto per Vercel
        result = mangum_handler(event, context)
        
        # Assicurati che la risposta sia nel formato corretto per Vercel
        if isinstance(result, dict):
            # Se ha già statusCode, è già nel formato corretto
            if "statusCode" in result:
                return result
            # Se è un dict ma senza statusCode, potrebbe essere il body
            elif "body" in result or "headers" in result:
                # Aggiungi statusCode se mancante
                if "statusCode" not in result:
                    result["statusCode"] = 200
                return result
            else:
                # Dict semplice, convertilo in body JSON
                import json
                return {
                    "statusCode": 200,
                    "headers": {"Content-Type": "application/json"},
                    "body": json.dumps(result)
                }
        elif isinstance(result, str):
            # Stringa, potrebbe essere già JSON serializzato
            return {
                "statusCode": 200,
                "headers": {"Content-Type": "application/json"},
                "body": result
            }
        else:
            # Altro tipo, serializza come JSON
            import json
            return {
                "statusCode": 200,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps(result)
            }
    except Exception as e:
        print(f"ERROR in handler: {str(e)}")
        print(f"ERROR traceback: {traceback.format_exc()}")
        import json
        error_info = {
            "error": "Serverless function execution failed",
            "message": str(e),
            "path": event.get("path", "unknown") if event else "no event"
        }
        if os.getenv("VERCEL_ENV") != "production":
            error_info["traceback"] = traceback.format_exc()
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(error_info)
        }

