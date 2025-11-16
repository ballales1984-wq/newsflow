"""Verifica e corregge configurazione WSGI"""
import requests
import json

BASE_URL = 'https://www.pythonanywhere.com/api/v0/user/braccobaldo'
HEADERS = {'Authorization': 'Token f17e14d4b1a12e0bf325cc0c1d8f9871fe50e599'}
DOMAIN = 'braccobaldo.pythonanywhere.com'

print("="*60)
print("🔧 Verifica e correzione configurazione WSGI")
print("="*60)

# 1. Verifica configurazione webapp
print("\n1️⃣  Verifica configurazione webapp...")
r = requests.get(f'{BASE_URL}/webapps/{DOMAIN}/', headers=HEADERS)
if r.status_code == 200:
    config = r.json()
    print(f"   ✅ Source directory: {config.get('source_directory')}")
    print(f"   ✅ Python version: {config.get('python_version')}")
else:
    print(f"   ❌ Errore: {r.status_code}")

# 2. Verifica file WSGI
print("\n2️⃣  Verifica file WSGI...")
r = requests.get(f'{BASE_URL}/files/path/home/braccobaldo/newsflow/backend/wsgi.py', headers=HEADERS)
if r.status_code == 200:
    print("   ✅ wsgi.py esiste")
    content = r.text
    print(f"   Dimensione: {len(content)} caratteri")
else:
    print(f"   ⚠️  wsgi.py non trovato (Status: {r.status_code})")
    print("   Creazione wsgi.py...")
    
    wsgi_content = """import sys
import os

path = "/home/braccobaldo/newsflow/backend"
if path not in sys.path:
    sys.path.insert(0, path)

os.chdir(path)

from app.main_simple import app
application = app
"""
    
    files = {'content': ('wsgi.py', wsgi_content)}
    r2 = requests.post(
        f'{BASE_URL}/files/path/home/braccobaldo/newsflow/backend/wsgi.py',
        headers=HEADERS,
        files=files
    )
    if r2.status_code in [200, 201]:
        print("   ✅ wsgi.py creato!")
    else:
        print(f"   ❌ Errore creazione: {r2.status_code}")

# 3. Verifica file app
print("\n3️⃣  Verifica file app...")
r = requests.get(f'{BASE_URL}/files/path/home/braccobaldo/newsflow/backend/app/main_simple.py', headers=HEADERS)
if r.status_code == 200:
    print("   ✅ app/main_simple.py esiste")
else:
    print(f"   ❌ app/main_simple.py non trovato (Status: {r.status_code})")

# 4. Reload
print("\n4️⃣  Reload webapp...")
r = requests.post(f'{BASE_URL}/webapps/{DOMAIN}/reload/', headers=HEADERS)
if r.status_code == 200:
    print("   ✅ Reload completato!")
else:
    print(f"   ⚠️  Errore reload: {r.status_code}")

print("\n" + "="*60)
print("✅ Verifica completata!")
print("="*60)
print(f"\n🌐 URL: https://{DOMAIN}")
print(f"🧪 Test: https://{DOMAIN}/api/v1/articles?limit=1")
print("\n💡 Se ancora 404, verifica manualmente:")
print("   1. Dashboard → Web → WSGI configuration file")
print("   2. Assicurati che punti a: /home/braccobaldo/newsflow/backend/wsgi.py")

