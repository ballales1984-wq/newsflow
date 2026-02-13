
import os
os.environ["DATABASE_URL"] = "sqlite:///./newsflow.db"
os.environ["SECRET_KEY"] = "dev-key"

from app.services.collectors.rss_collector import RSSCollector, RSS_SOURCES
import json
from datetime import datetime

# Custom JSON encoder per gestire datetime
class DateTimeEncoder(json.JSONEncoder):
collector = RSSCollector()
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

print("🔍 Raccogliendo notizie VERE da fonti RSS... - collect_news_now.py:17")
print("= - collect_news_now.py:18" * 50)
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
    print(f"\n📡 Raccogliendo da: {name} - collect_news_now.py:31")
    print(f"URL: {url} - collect_news_now.py:32")

    try:
        articles = collector.collect(url, max_articles=3)
        print(f"✅ Trovate {len(articles)} notizie - collect_news_now.py:36")

        for article in articles:
            article['source_name'] = name
            all_articles.append(article)
            print(f"{article['title'][:60]}... - collect_news_now.py:41")

    except Exception as e:
        print(f"❌ Errore: {e} - collect_news_now.py:44")

print("\n - collect_news_now.py:46" + "=" * 50)
print(f"📊 TOTALE: {len(all_articles)} notizie raccolte! - collect_news_now.py:47")

# Salva in JSON per vedere
with open('notizie_vere.json', 'w', encoding='utf-8') as f:
    json.dump(all_articles, f, indent=2, ensure_ascii=False)

print(f"💾 Salvate in: notizie_vere.json - collect_news_now.py:53")
print("\n✨ Ora possiamo usarle nell'app! - collect_news_now.py:54")

