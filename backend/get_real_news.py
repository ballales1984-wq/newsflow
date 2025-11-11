"""Script standalone per raccogliere notizie VERE - zero dipendenze app"""
import feedparser
import json
from datetime import datetime

print("🔍 Raccogliendo notizie VERE da RSS...")
print("=" * 60)

RSS_FEEDS = {
    'The Guardian Tech': 'https://www.theguardian.com/technology/rss',
    'Wired IT': 'https://www.wired.it/feed/rss',
    'The Hacker News': 'https://feeds.feedburner.com/TheHackersNews',
    'Punto Informatico': 'https://www.punto-informatico.it/feed/',
}

all_articles = []
article_id = 1

for source_name, rss_url in RSS_FEEDS.items():
    print(f"\n📡 {source_name}")
    print(f"   {rss_url}")
    
    try:
        feed = feedparser.parse(rss_url)
        count = 0
        
        for entry in feed.entries[:3]:  # Prime 3 per fonte
            article = {
                "id": article_id,
                "title": entry.get('title', '').strip(),
                "slug": entry.get('title', '').lower().replace(' ', '-')[:50],
                "url": entry.get('link', ''),
                "summary": entry.get('summary', '')[:300] + "...",
                "author": entry.get('author', source_name),
                "published_at": datetime.now().isoformat(),
                "collected_at": datetime.now().isoformat(),
                "source_id": 1,
                "is_featured": count == 0,  # Prima di ogni fonte = featured
                "is_verified": True,
                "is_archived": False,
                "quality_score": 0.75 + (count * 0.05),
                "reading_time_minutes": 3 + count,
                "keywords": ["tech", "news", "real"],
                "language": "en"
            }
            
            all_articles.append(article)
            print(f"   ✅ {article['title'][:70]}...")
            
            article_id += 1
            count += 1
            
    except Exception as e:
        print(f"   ❌ Errore: {e}")

print("\n" + "=" * 60)
print(f"📊 Raccolte {len(all_articles)} notizie VERE!")
print("\n💾 Salvando...")

# Salva JSON
with open('real_news.json', 'w', encoding='utf-8') as f:
    json.dump({
        "items": all_articles,
        "total": len(all_articles),
        "page": 1,
        "size": 20,
        "pages": 1
    }, f, indent=2, ensure_ascii=False)

print(f"✅ Salvate in: real_news.json")
print("\n🎯 Ora aggiorno main_simple.py con queste notizie!")

