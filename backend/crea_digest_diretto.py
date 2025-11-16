"""Crea digest direttamente senza eseguire script esterni"""
import json
import os
from datetime import datetime, timedelta
from collections import defaultdict

# Mappa category_id -> nome categoria
CATEGORY_MAP = {
    1: "Tecnologia",
    2: "Scienza",
    3: "Filosofia",
    4: "Cybersecurity",
    5: "Intelligenza Artificiale",
    6: "Innovazione",
    7: "Cultura",
    8: "Etica",
    9: "Sport",
    10: "Natura & Ambiente",
    11: "Business & Economia",
    12: "Salute",
    13: "Politica",
    14: "Intrattenimento"
}

CATEGORY_EMOJI = {
    1: "💻", 2: "🔬", 3: "🤔", 4: "🔒", 5: "🤖", 6: "💡", 7: "🎨",
    8: "⚖️", 9: "⚽", 10: "🌍", 11: "💼", 12: "🏥", 13: "🏛️", 14: "🎬"
}

# Carica articoli
json_path = os.path.join('backend', 'final_news_italian.json')
if not os.path.exists(json_path):
    json_path = 'final_news_italian.json'

with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)
    articles = data.get('items', [])

# Filtra articoli di oggi
today = datetime.now().date()
yesterday = today - timedelta(days=1)
today_articles = []

for article in articles:
    published_at = article.get('published_at', '')
    if not published_at:
        continue
    
    try:
        if isinstance(published_at, str) and 'T' in published_at:
            date_str = published_at.split('T')[0]
            article_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            if article_date >= yesterday:
                today_articles.append(article)
    except:
        continue

print(f"Articoli di oggi: {len(today_articles)}")

# Raggruppa per categoria (default 1 se non presente)
articles_by_category = defaultdict(list)
for article in today_articles:
    category_id = article.get('category_id', 1)
    if len(articles_by_category[category_id]) < 5:
        summary = article.get('summary', '')
        # Rimuovi HTML tags
        import re
        summary_clean = re.sub(r'<[^>]+>', '', summary)[:200]
        articles_by_category[category_id].append({
            'title': article.get('title', ''),
            'description': summary_clean
        })

# Costruisci digest
digest_categories = []
for category_id in sorted(articles_by_category.keys()):
    category_name = CATEGORY_MAP.get(category_id, "Tecnologia")
    emoji = CATEGORY_EMOJI.get(category_id, "📰")
    if articles_by_category[category_id]:
        digest_categories.append({
            'category': f"{emoji} {category_name}",
            'articles': articles_by_category[category_id]
        })

digest_data = {
    'date': datetime.now().strftime("%Y-%m-%d"),
    'digest': digest_categories
}

# Salva in tutte le posizioni
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
paths = [
    os.path.join(project_root, 'backend', 'digest.json'),
    os.path.join(project_root, 'api', 'digest.json'),
    os.path.join(project_root, 'frontend', 'src', 'assets', 'digest.json')
]

for path in paths:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(digest_data, f, indent=2, ensure_ascii=False)
    print(f"✅ Salvato: {os.path.relpath(path, project_root)}")

print(f"\n✅ Digest generato: {len(digest_categories)} categorie, {sum(len(c['articles']) for c in digest_categories)} articoli")

