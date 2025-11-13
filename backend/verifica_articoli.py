"""Verifica quanti articoli ci sono nel file"""
import json
import os

paths = [
    'backend/final_news_italian.json',
    'api/final_news_italian.json',
    'final_news_italian.json'
]

for path in paths:
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            articles = data.get('items', [])
            print(f"✅ {path}: {len(articles)} articoli")
            if len(articles) > 0:
                print(f"   Primo articolo: {articles[0].get('title', 'N/A')[:60]}...")
                print(f"   Ultimo aggiornamento: {data.get('updated_at', 'N/A')}")
        break
else:
    print("❌ Nessun file trovato!")

