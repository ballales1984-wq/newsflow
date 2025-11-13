"""
Test endpoint semplice per verificare che Vercel riconosca i file Python
"""
import json
import traceback

def handler(event, context):
    """Handler per Vercel serverless functions"""
    try:
        print("DEBUG: Test endpoint handler called")
        print(f"DEBUG: event={event}")
        print(f"DEBUG: context={context}")
        
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "message": "API test endpoint works!",
                "path": event.get("path", "unknown") if event else "no event",
                "method": event.get("httpMethod", "unknown") if event else "no event"
            })
        }
    except Exception as e:
        print(f"ERROR in test handler: {str(e)}")
        print(f"ERROR traceback: {traceback.format_exc()}")
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "error": "Test endpoint failed",
                "message": str(e),
                "traceback": traceback.format_exc()
            })
        }

