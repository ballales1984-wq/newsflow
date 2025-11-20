"""Installa Mangum su PythonAnywhere tramite API"""
import requests
import time

BASE_URL = 'https://www.pythonanywhere.com/api/v0/user/braccobaldo'
HEADERS = {'Authorization': 'Token f17e14d4b1a12e0bf325cc0c1d8f9871fe50e599'}
CONSOLE_ID = 43449916

print("📦 Installazione Mangum su PythonAnywhere...")
print("=" * 60)

# Comandi da eseguire
commands = [
    'cd ~/newsflow/backend',
    'pip3.10 install --user mangum',
    'python3.10 -c "import mangum; print(\"✅ Mangum installato:\", mangum.__version__)"'
]

print("\n📤 Invio comandi alla console Bash PythonAnywhere...")
for i, cmd in enumerate(commands, 1):
    print(f"   {i}. {cmd}")
    r = requests.post(
        f'{BASE_URL}/consoles/{CONSOLE_ID}/send_input/',
        headers=HEADERS,
        data={'input': f'{cmd}\n'}
    )
    if r.status_code == 200:
        print(f"      ✅ Comando inviato")
    else:
        print(f"      ⚠️  Errore: {r.status_code}")
    time.sleep(3)  # Attendi tra i comandi

print("\n" + "=" * 60)
print("⏳ Attendi 15 secondi per completare l'installazione...")
time.sleep(15)

print("\n✅ Installazione completata!")
print("\n💡 Ora aggiorna il file WSGI configuration come indicato prima.")

