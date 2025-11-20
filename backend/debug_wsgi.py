"""Debug completo WSGI e dipendenze"""
import requests

BASE_URL = 'https://www.pythonanywhere.com/api/v0/user/braccobaldo'
HEADERS = {'Authorization': 'Token f17e14d4b1a12e0bf325cc0c1d8f9871fe50e599'}
CONSOLE_ID = 43449916

print("🔍 Debug completo configurazione...")
print("=" * 70)

# 1. Verifica Mangum
print("\n1️⃣  Verifica Mangum...")
commands = [
    'cd ~/newsflow/backend',
    'python3.10 -c "import mangum; print(\"Mangum OK:\", mangum.__version__)"'
]
for cmd in commands:
    r = requests.post(
        f'{BASE_URL}/consoles/{CONSOLE_ID}/send_input/',
        headers=HEADERS,
        data={'input': f'{cmd}\n'}
    )
    import time
    time.sleep(2)

# 2. Verifica app FastAPI
print("\n2️⃣  Verifica app FastAPI...")
commands = [
    'cd ~/newsflow/backend',
    'python3.10 -c "from app.main_simple import app; print(\"App OK:\", type(app))"'
]
for cmd in commands:
    r = requests.post(
        f'{BASE_URL}/consoles/{CONSOLE_ID}/send_input/',
        headers=HEADERS,
        data={'input': f'{cmd}\n'}
    )
    import time
    time.sleep(2)

# 3. Test Mangum + FastAPI insieme
print("\n3️⃣  Test Mangum + FastAPI...")
test_code = '''
import sys
sys.path.insert(0, '/home/braccobaldo/newsflow/backend')
import os
os.chdir('/home/braccobaldo/newsflow/backend')
from mangum import Mangum
from app.main_simple import app
handler = Mangum(app, lifespan="off")
print("✅ Mangum handler creato:", type(handler))
'''
cmd = f'python3.10 -c "{test_code.replace(chr(10), "; ")}"'
r = requests.post(
    f'{BASE_URL}/consoles/{CONSOLE_ID}/send_input/',
    headers=HEADERS,
    data={'input': f'{cmd}\n'}
)
import time
time.sleep(3)

print("\n" + "=" * 70)
print("✅ Comandi di debug inviati alla console")
print("💡 Controlla la console Bash su PythonAnywhere per vedere i risultati")

