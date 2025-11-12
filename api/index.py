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
    
    # Verifica file JSON
    json_path = os.path.join(project_root, 'backend', 'final_news_italian.json')
    print(f"DEBUG: final_news exists={os.path.exists(json_path)}")
    if os.path.exists(json_path):
        print(f"DEBUG: final_news size={os.path.getsize(json_path)}")

    # Import con gestione errori
    print("DEBUG: Importing mangum...")
    from mangum import Mangum
    print("DEBUG: Mangum imported successfully")
    
    print("DEBUG: Importing app.main_simple...")
    from app.main_simple import app
    print("DEBUG: app.main_simple imported successfully")

    # Crea handler Mangum per Vercel
    handler = Mangum(app, lifespan="off")
    print("DEBUG: Mangum handler created successfully")

except Exception as e:
    print(f"ERROR during initialization: {str(e)}")
    print(f"ERROR traceback: {traceback.format_exc()}")
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
    handler = error_handler

def lambda_handler(event, context):
    """Handler per Vercel serverless functions"""
    try:
        return handler(event, context)
    except Exception as e:
        print(f"ERROR in lambda_handler: {str(e)}")
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

