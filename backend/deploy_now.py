"""Esegui deploy immediato"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from setup_pythonanywhere_api import *

print("\n" + "="*60)
print("🚀 DEPLOY AUTOMATICO SU PYTHONANYWHERE")
print("="*60)

# Verifica token
if not check_token():
    sys.exit(1)

# Nota: Clone repository manualmente
print("\n⚠️  IMPORTANTE: Clona repository manualmente:")
print("   1. Vai su: https://www.pythonanywhere.com/user/braccobaldo/")
print("   2. Consoles → Bash")
print("   3. Esegui: cd ~ && git clone https://github.com/ballales1984-wq/newsflow.git")
print("   4. Esegui: cd newsflow/backend && pip3.10 install --user -r requirements.txt")
print("\nPremi Enter quando hai clonato il repository...")
input()

# Esegui setup
create_wsgi_file()
create_webapp()
configure_webapp()
reload_webapp()

print("\n" + "="*60)
print("✅ DEPLOY COMPLETATO!")
print("="*60)

