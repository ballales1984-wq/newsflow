"""Verifica repository e reload webapp"""
import requests
import time

BASE_URL = 'https://www.pythonanywhere.com/api/v0/user/braccobaldo'
HEADERS = {'Authorization': 'Token f17e14d4b1a12e0bf325cc0c1d8f9871fe50e599'}
DOMAIN = 'braccobaldo.pythonanywhere.com'

print("🔍 Verifica repository...")
r = requests.get(f'{BASE_URL}/files/tree/?path=/home/braccobaldo/newsflow', headers=HEADERS)
if r.status_code == 200:
    print("✅ Repository clonato!")
    files = r.json()
    print(f"   File trovati: {len(files)}")
else:
    print(f"⚠️  Repository non ancora clonato (Status: {r.status_code})")
    print("   Verifica nella console PythonAnywhere se il clone è in corso...")

print("\n🔄 Reload webapp...")
r = requests.post(f'{BASE_URL}/webapps/{DOMAIN}/reload/', headers=HEADERS)
if r.status_code == 200:
    print("✅ Reload completato!")
else:
    print(f"⚠️  Errore reload: {r.status_code}")

print(f"\n🌐 URL: https://{DOMAIN}")
print(f"🧪 Test: https://{DOMAIN}/api/v1/articles?limit=1")

