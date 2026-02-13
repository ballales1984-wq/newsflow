"""Script per raccogliere notizie VERE immediatamente"""
import os
os.environ["DATABASE_URL"] = "sqlite:///./newsflow.db"
os.environ["SECRET_KEY"] = "dev-key"

from app.services.collectors.rss_collector import RSSCollector, RSS_SOURCES
import json
from datetime import datetime

# Custom JSON encoder per gestire datetime
class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

print("Raccogliendo notizie da fonti RSS... - collect_news_now.py:17")
print("= - collect_news_now.py:18" * 50)

collector = RSSCollector()
all_articles = []

# Raccoglie da 5 fonti principali
sources_to_try = [
    ('The Guardian Tech', RSS_SOURCES['theguardian_tech']),
    ('Wired Italia', RSS_SOURCES['wired_it']),
    ('The Hacker News', RSS_SOURCES['the_hacker_news']),
    ('MIT Tech Review', RSS_SOURCES['mit_tech_review']),
    ('Punto Informatico', RSS_SOURCES['punto_informatico']),
]

for name, url in sources_to_try:
    print(f"\nRaccogliendo da: {name} - collect_news_now.py:33")
    print(f"URL: {url} - collect_news_now.py:34")

    try:
        articles = collector.collect(url, max_articles=3)
        print(f"Trovate {len(articles)} notizie - collect_news_now.py:38")

        for article in articles:
            article['source_name'] = name
            all_articles.append(article)
            print(f"{article['title'][:60]}... - collect_news_now.py:43")

    except Exception as e:
        print(f"Errore: {e} - collect_news_now.py:46")

print("\n - collect_news_now.py:48" + "=" * 50)
print(f"TOTALE: {len(all_articles)} notizie raccolte! - collect_news_now.py:49")

# Salva in JSON per vedere
with open('notizie_vere.json', 'w', encoding='utf-8') as f:
    json.dump(all_articles, f, indent=2, ensure_ascii=False, cls=DateTimeEncoder)

print(f"Salvate in: notizie_vere.json - collect_news_now.py:55")
print("\nOra possiamo usarle nell'app! - collect_news_now.py:56")

