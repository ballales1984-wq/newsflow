"""Script rapido per generare digest ora"""
import json
import os
import sys
from datetime import datetime, timedelta
from collections import defaultdict

# Importa le funzioni dallo script originale
sys.path.insert(0, os.path.dirname(__file__))
from genera_digest_giornaliero import generate_digest, save_digest

if __name__ == '__main__':
    print("Generazione digest...")
    digest = generate_digest()
    if digest:
        save_digest(digest)
        print("✅ Digest generato!")
    else:
        print("❌ Errore generazione digest")
        sys.exit(1)

