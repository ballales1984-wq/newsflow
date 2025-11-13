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

    # Import con gestione errori
    print("DEBUG: Importing mangum...")
    from mangum import Mangum
    print("DEBUG: Mangum imported successfully")
    
    print("DEBUG: Importing app.main_simple...")
    from app.main_simple import app
    print("DEBUG: app.main_simple imported successfully")

    # Crea handler Mangum per Vercel
    mangum_handler = Mangum(app, lifespan="off")
    print("DEBUG: Mangum handler created successfully")

except Exception as e:
    print(f"ERROR during initialization: {str(e)}")
    print(f"ERROR traceback: {traceback.format_exc()}")
    import json
    # Crea un handler di fallback che restituisce un errore
    def error_handler(event, context):
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "error": "Serverless function initialization failed",
                "message": str(e),
                "traceback": traceback.format_exc()
            })
        }
    mangum_handler = error_handler

def handler(event, context):
    """Handler per Vercel serverless functions"""
    try:
        return mangum_handler(event, context)
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

