"""Test per verificare quanti articoli restituisce il backend"""
import requests
import json

try:
    response = requests.get('http://localhost:8000/api/v1/articles?limit=200', timeout=5)
    if response.status_code == 200:
        data = response.json()
        total = data.get('total', 0)
        items = data.get('items', [])
        print(f"✅ Backend locale risponde:")
        print(f"   - Total articoli: {total}")
        print(f"   - Items restituiti: {len(items)}")
        if items:
            print(f"   - Primo articolo: {items[0].get('title', 'N/A')[:60]}...")
    else:
        print(f"❌ Errore: {response.status_code}")
except Exception as e:
    print(f"❌ Errore connessione: {e}")

