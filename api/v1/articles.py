"""
Test endpoint per /api/v1/articles
Verifica che Vercel riconosca le serverless functions
"""
import json

def handler(event, context):
    """Handler per Vercel serverless functions"""
    try:
        print(f"DEBUG: Handler called for /api/v1/articles")
        print(f"DEBUG: event={event}")
        print(f"DEBUG: context={context}")
        
        # Risposta di test
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({
                "message": "API endpoint works!",
                "path": event.get("path", "unknown") if event else "no event",
                "method": event.get("httpMethod", "unknown") if event else "no event",
                "test": True
            })
        }
    except Exception as e:
        print(f"ERROR in handler: {str(e)}")
        import traceback
        print(f"ERROR traceback: {traceback.format_exc()}")
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "error": "Test endpoint failed",
                "message": str(e)
            })
        }

