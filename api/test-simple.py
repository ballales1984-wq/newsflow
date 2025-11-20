"""
Test endpoint semplice per verificare che Vercel funzioni
"""
import json

def handler(event, context):
    """Handler di test semplice"""
    try:
        print(f"🔍 TEST: Event type={type(event)}")
        print(f"🔍 TEST: Event keys={list(event.keys()) if isinstance(event, dict) else 'not a dict'}")
        print(f"🔍 TEST: Event={json.dumps(event, default=str)[:500]}")
        
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({
                "message": "Test endpoint works!",
                "event_type": str(type(event)),
                "event_keys": list(event.keys()) if isinstance(event, dict) else None,
                "path": event.get("path", "unknown") if isinstance(event, dict) else "unknown"
            })
        }
    except Exception as e:
        import traceback
        print(f"❌ TEST ERROR: {str(e)}")
        print(f"❌ TEST TRACEBACK: {traceback.format_exc()}")
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "error": "Test endpoint failed",
                "message": str(e),
                "traceback": traceback.format_exc()
            })
        }

