#!/usr/bin/env python3
"""Script rapido per aggiornare il digest con la data odierna e articoli attuali"""
import json
import os
from datetime import datetime

# Carica gli articoli salvati da PowerShell
articles = []
try:
    with open('c:/Users/user/news/temp_articles.json', 'r', encoding='utf-8') as f:
        articles = json.load(f)
except:
    print("❌ Errore nel caricamento articoli temporanei - update_digest_today.py:13")
    exit(1)

print(f"📰 Caricati {len(articles)} articoli - update_digest_today.py:16")

# Categorie disponibili
CATEGORIES = {
    "💻 Tecnologia": ["technology", "tech", "computer", "software", "app", "quantum"],
    "🤖 Intelligenza Artificiale": ["ai", "artificial intelligence", "chatgpt", "gpt", "machine learning", "llm", "deepmind"],
    "🔒 Cybersecurity": ["security", "cyber", "breach", "hack", "malware", "exploit"],
    "🔬 Scienza": ["science", "research", "discovery", "study", "physics", "biology"],
    "💼 Business": ["business", "economy", "market", "company", "startup", "finance"],
    "🌍 Politica": ["politics", "government", "election", "parliament", "biden", "trump"],
    "🎬 Intrattenimento": ["film", "movie", "music", "entertainment", "celebrity", "oscar"],
    "🏥 Salute": ["health", "medical", "vaccine", "disease", "doctor"],
}

def categorize_article(article):
    """Assegna una categoria in base a title e content"""
    title = (article.get('title', '') + ' ' + article.get('summary', '')).lower()

    for category, keywords in CATEGORIES.items():
        if any(kw in title for kw in keywords):
            return category

    return "💻 Tecnologia"  # fallback

# Raggruppa articoli per categoria
categorized = {}
for article in articles[:50]:  # Prendi i primi 50
    cat = categorize_article(article)
    if cat not in categorized:
        categorized[cat] = []

    categorized[cat].append({
        "title": article.get('title', '')[:100],
        "description": article.get('summary', '')[:150]
    })

# Costruisci il digest
digest = {
    "date": datetime.now().strftime("%Y-%m-%d"),
    "digest": []
}

for category, category_articles in categorized.items():
    digest["digest"].append({
        "category": category,
        "articles": category_articles[:5]  # Max 5 articoli per categoria
    })

# Salva il digest in tutti i path
paths = [
    'c:/Users/user/news/frontend/src/assets/digest.json',
    'c:/Users/user/news/api/digest.json',
    'c:/Users/user/news/backend/digest.json'
]

for path in paths:
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(digest, f, ensure_ascii=False, indent=2)
        print(f"✅ Digest salvato in: {path} - update_digest_today.py:76")
    except Exception as e:
        print(f"⚠️  Errore salvataggio {path}: {e} - update_digest_today.py:78")

print(f"\n✅ Digest aggiornato con data: {digest['date']} - update_digest_today.py:80")
print(f"Categorie: {len(digest['digest'])} - update_digest_today.py:81")
for cat_obj in digest['digest']:
    print(f"{cat_obj['category']}: {len(cat_obj['articles'])} articoli - update_digest_today.py:83")
