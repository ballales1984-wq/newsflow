"""Script per raccogliere notizie VERE immediatamente"""
import os
os.environ["DATABASE_URL"] = "sqlite:///./newsflow.db"
os.environ["SECRET_KEY"] = "dev-key"

from app.services.collectors.rss_collector import RSSCollector, RSS_SOURCES
import json

print("🔍 Raccogliendo notizie VERE da fonti RSS...")
print("=" * 50)

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
    print(f"\n📡 Raccogliendo da: {name}")
    print(f"   URL: {url}")
    
    try:
        articles = collector.collect(url, max_articles=3)
        print(f"   ✅ Trovate {len(articles)} notizie")
        
        for article in articles:
            article['source_name'] = name
            all_articles.append(article)
            print(f"   - {article['title'][:60]}...")
            
    except Exception as e:
        print(f"   ❌ Errore: {e}")

print("\n" + "=" * 50)
print(f"📊 TOTALE: {len(all_articles)} notizie raccolte!")

# Salva in JSON per vedere
with open('notizie_vere.json', 'w', encoding='utf-8') as f:
    json.dump(all_articles, f, indent=2, ensure_ascii=False)

print(f"💾 Salvate in: notizie_vere.json")
print("\n✨ Ora possiamo usarle nell'app!")

