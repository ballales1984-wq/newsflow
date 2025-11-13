def handler(event, context):
    import json
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"message": "API test endpoint works!", "path": event.get("path", "unknown")})
    }
