"""
Endpoint di test minimo per verificare che Vercel funzioni
Non dipende da FastAPI o altre librerie complesse
"""
import json
import os

def handler(event, context):
    """Handler di test minimo"""
    try:
        # Informazioni di base
        info = {
            "status": "ok",
            "message": "Test endpoint funziona!",
            "python_version": os.sys.version,
            "cwd": os.getcwd(),
            "vercel": os.getenv("VERCEL") == "1",
            "path": event.get("path", "unknown") if event else "no event",
            "method": event.get("httpMethod", "unknown") if event else "no event"
        }
        
        # Verifica file JSON
        json_paths = [
            os.path.join(os.getcwd(), 'api', 'final_news_italian.json'),
            os.path.join(os.getcwd(), 'backend', 'final_news_italian.json'),
            os.path.join(os.getcwd(), 'final_news_italian.json'),
        ]
        
        info["json_files"] = {}
        for path in json_paths:
            exists = os.path.exists(path)
            info["json_files"][path] = {
                "exists": exists,
                "size": os.path.getsize(path) if exists else None
            }
        
        # Lista directory
        try:
            cwd = os.getcwd()
            info["directories"] = {
                "cwd": cwd,
                "files_in_cwd": os.listdir(cwd)[:10] if os.path.exists(cwd) else [],
                "api_exists": os.path.exists(os.path.join(cwd, 'api')),
                "backend_exists": os.path.exists(os.path.join(cwd, 'backend')),
            }
            if os.path.exists(os.path.join(cwd, 'api')):
                info["directories"]["files_in_api"] = os.listdir(os.path.join(cwd, 'api'))[:10]
        except Exception as e:
            info["directory_error"] = str(e)
        
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps(info, indent=2)
        }
    except Exception as e:
        import traceback
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "error": "Test endpoint failed",
                "message": str(e),
                "traceback": traceback.format_exc()
            })
        }
