"""Controlla log errori PythonAnywhere"""
import requests

BASE_URL = 'https://www.pythonanywhere.com/api/v0/user/braccobaldo'
HEADERS = {'Authorization': 'Token f17e14d4b1a12e0bf325cc0c1d8f9871fe50e599'}
DOMAIN = 'braccobaldo.pythonanywhere.com'

print("="*60)
print("📋 Controllo Log Errori PythonAnywhere")
print("="*60)

# Ottieni info webapp
print("\n1️⃣  Info webapp...")
r = requests.get(f'{BASE_URL}/webapps/{DOMAIN}/', headers=HEADERS)
if r.status_code == 200:
    config = r.json()
    print(f"   ✅ Webapp trovata")
    print(f"   Source: {config.get('source_directory')}")
    print(f"   Python: {config.get('python_version')}")
else:
    print(f"   ❌ Errore: {r.status_code}")

# Prova a leggere log errori comuni
log_paths = [
    '/var/www/braccobaldo_pythonanywhere_com_wsgi.py.log',
    '/var/log/braccobaldo.pythonanywhere.com.error.log',
    '/home/braccobaldo/newsflow/backend/error.log'
]

print("\n2️⃣  Cerca log errori...")
for log_path in log_paths:
    r = requests.get(f'{BASE_URL}/files/path{log_path}', headers=HEADERS)
    if r.status_code == 200:
        print(f"\n   ✅ Log trovato: {log_path}")
        content = r.text
        print(f"   Ultime 50 righe:")
        lines = content.split('\n')[-50:]
        for line in lines:
            if line.strip():
                print(f"   {line}")
        break
    else:
        print(f"   ⚠️  {log_path}: {r.status_code}")

# Verifica file necessari
print("\n3️⃣  Verifica file necessari...")
files_to_check = [
    '/home/braccobaldo/newsflow/backend/app/main_simple.py',
    '/home/braccobaldo/newsflow/backend/requirements.txt',
    '/home/braccobaldo/newsflow/backend/final_news_italian.json'
]

for file_path in files_to_check:
    r = requests.get(f'{BASE_URL}/files/path{file_path}', headers=HEADERS)
    status = "✅" if r.status_code == 200 else "❌"
    print(f"   {status} {file_path.split('/')[-1]}")

print("\n" + "="*60)
print("💡 Se vedi errori, controlla:")
print("   1. WSGI configuration file punta al path corretto")
print("   2. Tutte le dipendenze sono installate")
print("   3. File JSON esiste")
print("="*60)

