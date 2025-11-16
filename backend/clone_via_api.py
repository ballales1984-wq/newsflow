"""Clona repository via API console"""
import requests
import time

BASE_URL = 'https://www.pythonanywhere.com/api/v0/user/braccobaldo'
HEADERS = {'Authorization': 'Token f17e14d4b1a12e0bf325cc0c1d8f9871fe50e599'}
CONSOLE_ID = 43449916

commands = [
    'cd ~',
    'git clone https://github.com/ballales1984-wq/newsflow.git',
    'cd newsflow/backend',
    'pip3.10 install --user fastapi uvicorn pydantic pydantic-settings python-multipart python-slugify mangum',
    'ls -la',
    'echo "✅ Setup completato!"'
]

print("🚀 Invio comandi alla console...")
for i, cmd in enumerate(commands, 1):
    print(f"\n[{i}/{len(commands)}] Eseguendo: {cmd}")
    response = requests.post(
        f'{BASE_URL}/consoles/{CONSOLE_ID}/send_input/',
        headers=HEADERS,
        data={'input': f'{cmd}\n'}
    )
    if response.status_code == 200:
        print("   ✅ Comando inviato")
    else:
        print(f"   ⚠️  Status: {response.status_code}")
    time.sleep(2)  # Attendi tra i comandi

print("\n✅ Tutti i comandi inviati!")
print("\n⏳ Attendi 30-60 secondi per il clone...")
print("   Poi esegui: python verifica_e_reload.py")

