"""Verifica WSGI configuration e Mangum"""
import requests

BASE_URL = 'https://www.pythonanywhere.com/api/v0/user/braccobaldo'
HEADERS = {'Authorization': 'Token f17e14d4b1a12e0bf325cc0c1d8f9871fe50e599'}
CONSOLE_ID = 43449916

print("🔍 Verifica configurazione WSGI...")
print("=" * 60)

# 1. Verifica Mangum installato
print("\n1️⃣  Verifica Mangum installato...")
cmd = "python3.10 -c 'import mangum; print(\"OK: Mangum\", mangum.__version__)'"
r = requests.post(
    f'{BASE_URL}/consoles/{CONSOLE_ID}/send_input/',
    headers=HEADERS,
    data={'input': f'{cmd}\n'}
)
print("   ✅ Comando inviato alla console")

# 2. Verifica file WSGI (non possiamo leggerlo direttamente, ma possiamo verificare se esiste)
print("\n2️⃣  Verifica webapp...")
r = requests.get(
    f'{BASE_URL}/webapps/',
    headers=HEADERS
)
if r.status_code == 200:
    webapps = r.json()
    for webapp in webapps:
        if 'braccobaldo.pythonanywhere.com' in webapp.get('domain_name', ''):
            print(f"   ✅ Webapp trovata: {webapp['domain_name']}")
            print(f"   Source: {webapp.get('source_directory', 'N/A')}")
            break

print("\n" + "=" * 60)
print("💡 Se Mangum non è installato, esegui:")
print("   pip3.10 install --user mangum")
print("\n💡 Se il file WSGI non usa Mangum, copia il contenuto di:")
print("   backend/WSGI_SEMPLICE.py")

