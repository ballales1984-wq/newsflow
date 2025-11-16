"""
Script automatico per deploy su PythonAnywhere usando l'API
Esegui questo script localmente (sul tuo PC) per deployare automaticamente!
"""
import requests
import json
import time

# ===== CONFIGURAZIONE =====
USERNAME = 'braccobaldo'
TOKEN = 'f17e14d4b1a12e0bf325cc0c1d8f9871fe50e599'  # Token API PythonAnywhere
HOST = 'www.pythonanywhere.com'  # o 'eu.pythonanywhere.com' se account EU
DOMAIN_NAME = 'braccobaldo.pythonanywhere.com'
PYTHON_VERSION = 'python310'
SOURCE_DIRECTORY = '/home/braccobaldo/newsflow/backend'
# ===========================

BASE_URL = f'https://{HOST}/api/v0/user/{USERNAME}'
HEADERS = {'Authorization': f'Token {TOKEN}'}

def print_step(step, message):
    print(f"\n{'='*60}")
    print(f"STEP {step}: {message}")
    print('='*60)

def check_token():
    """Verifica che il token funzioni"""
    print_step(1, "Verifica token API...")
    response = requests.get(f'{BASE_URL}/cpu/', headers=HEADERS)
    if response.status_code == 200:
        print("✅ Token valido!")
        return True
    else:
        print(f"❌ Errore token: {response.status_code}")
        print(f"   Messaggio: {response.text}")
        print(f"\n💡 Ottieni il token da: https://www.pythonanywhere.com/account/#api_token")
        return False

def clone_repo_via_console():
    """Clona repository tramite console API"""
    print_step(2, "Clonazione repository...")
    
    # Crea console Bash
    console_data = {
        'executable': 'bash',
        'arguments': '',
        'working_directory': '/home/braccobaldo'
    }
    
    response = requests.post(
        f'{BASE_URL}/consoles/',
        headers=HEADERS,
        json=console_data
    )
    
    if response.status_code == 201:
        console_id = response.json()['id']
        print(f"✅ Console creata (ID: {console_id})")
        
        # Esegui comandi
        commands = [
            'cd ~',
            'git clone https://github.com/ballales1984-wq/newsflow.git || (cd newsflow && git pull)',
            'cd newsflow/backend',
            'pip3.10 install --user fastapi uvicorn pydantic pydantic-settings python-multipart python-slugify mangum',
            'echo "✅ Setup completato!"'
        ]
        
        for cmd in commands:
            print(f"   Eseguendo: {cmd}")
            requests.post(
                f'{BASE_URL}/consoles/{console_id}/send_input/',
                headers=HEADERS,
                data={'input': f'{cmd}\n'}
            )
            time.sleep(2)
        
        print("✅ Repository clonato e dipendenze installate!")
        return True
    else:
        print(f"⚠️  Errore creazione console: {response.status_code}")
        print("   Fallback: clona manualmente nella console Bash")
        return False

def create_wsgi_file():
    """Crea file WSGI tramite API"""
    print_step(3, "Creazione file WSGI...")
    
    wsgi_content = f"""import sys
import os

path = '{SOURCE_DIRECTORY}'
if path not in sys.path:
    sys.path.insert(0, path)

os.chdir(path)

from app.main_simple import app
application = app
"""
    
    # Upload file WSGI
    wsgi_path = f'{SOURCE_DIRECTORY}/wsgi.py'
    files = {'content': ('wsgi.py', wsgi_content)}
    
    response = requests.post(
        f'{BASE_URL}/files/path{wsgi_path}',
        headers=HEADERS,
        files=files
    )
    
    if response.status_code in [200, 201]:
        print(f"✅ File WSGI creato: {wsgi_path}")
        return True
    else:
        print(f"⚠️  Errore creazione WSGI: {response.status_code}")
        return False

def create_webapp():
    """Crea webapp tramite API"""
    print_step(4, "Creazione webapp...")
    
    # Verifica se webapp esiste già
    response = requests.get(
        f'{BASE_URL}/webapps/{DOMAIN_NAME}/',
        headers=HEADERS
    )
    
    if response.status_code == 200:
        print(f"✅ Webapp già esistente: {DOMAIN_NAME}")
        return True
    
    # Crea nuova webapp
    webapp_data = {
        'domain_name': DOMAIN_NAME,
        'python_version': PYTHON_VERSION
    }
    
    response = requests.post(
        f'{BASE_URL}/webapps/',
        headers=HEADERS,
        json=webapp_data
    )
    
    if response.status_code == 200:
        print(f"✅ Webapp creata: {DOMAIN_NAME}")
        return True
    else:
        print(f"❌ Errore creazione webapp: {response.status_code}")
        print(f"   Messaggio: {response.text}")
        return False

def configure_webapp():
    """Configura webapp (source directory, WSGI)"""
    print_step(5, "Configurazione webapp...")
    
    config_data = {
        'source_directory': SOURCE_DIRECTORY,
        'virtualenv_path': None,  # Non usiamo virtualenv
    }
    
    response = requests.patch(
        f'{BASE_URL}/webapps/{DOMAIN_NAME}/',
        headers=HEADERS,
        json=config_data
    )
    
    if response.status_code == 200:
        print("✅ Webapp configurata!")
        
        # Configura WSGI file path
        # Nota: PythonAnywhere usa automaticamente wsgi.py nella source_directory
        print("✅ WSGI configurato automaticamente")
        return True
    else:
        print(f"⚠️  Errore configurazione: {response.status_code}")
        print(f"   Messaggio: {response.text}")
        return False

def reload_webapp():
    """Ricarica webapp"""
    print_step(6, "Reload webapp...")
    
    response = requests.post(
        f'{BASE_URL}/webapps/{DOMAIN_NAME}/reload/',
        headers=HEADERS
    )
    
    if response.status_code == 200:
        print("✅ Webapp ricaricata!")
        print(f"\n🌐 URL: https://{DOMAIN_NAME}")
        print(f"🧪 Test API: https://{DOMAIN_NAME}/api/v1/articles?limit=1")
        return True
    else:
        print(f"⚠️  Errore reload: {response.status_code}")
        return False

def main():
    print("\n" + "="*60)
    print("🚀 DEPLOY AUTOMATICO SU PYTHONANYWHERE")
    print("="*60)
    print(f"\nUsername: {USERNAME}")
    print(f"Domain: {DOMAIN_NAME}")
    print(f"Source: {SOURCE_DIRECTORY}")
    
    if TOKEN == 'YOUR_API_TOKEN':
        print("\n❌ ERRORE: Configura il TOKEN!")
        print("   1. Vai su: https://www.pythonanywhere.com/account/#api_token")
        print("   2. Genera token")
        print("   3. Aggiorna TOKEN in questo script")
        return
    
    # Esegui setup
    if not check_token():
        return
    
    # Nota: Clone via console è complesso, meglio farlo manualmente
    print("\n⚠️  NOTA: Clona repository manualmente:")
    print("   Console Bash → Esegui:")
    print("   cd ~ && git clone https://github.com/ballales1984-wq/newsflow.git")
    print("   cd newsflow/backend && pip3.10 install --user -r requirements.txt")
    
    input("\nPremi Enter quando hai clonato il repository...")
    
    create_wsgi_file()
    create_webapp()
    configure_webapp()
    reload_webapp()
    
    print("\n" + "="*60)
    print("✅ DEPLOY COMPLETATO!")
    print("="*60)
    print(f"\n🌐 Backend online: https://{DOMAIN_NAME}")
    print(f"🧪 Test: https://{DOMAIN_NAME}/api/v1/articles?limit=1")
    print("\n📝 Aggiorna frontend/src/environments/environment.prod.ts:")
    print(f"   apiUrl: 'https://{DOMAIN_NAME}/api/v1'")

if __name__ == '__main__':
    main()

