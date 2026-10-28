from app.main import app
from fastapi.routing import APIRoute

count = 0
def walk(r):
    global count
    for route in getattr(r, 'routes', []):
        if isinstance(route, APIRoute):
            print(route.path, route.methods)
            count += 1
        elif hasattr(route, 'routes'):
            walk(route)
walk(app)
print('total:' + str(count))
