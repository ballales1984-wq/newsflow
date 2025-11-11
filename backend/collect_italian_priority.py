"""Raccolta notizie con PRIORITÀ alle fonti ITALIANE"""
import feedparser
import json
from datetime import datetime

print("🇮🇹 Raccogliendo notizie - PRIORITÀ ITALIANE")
print("=" * 70)

# PRIMA: Fonti italiane (più notizie)
ITALIAN_SOURCES = {
    'MicroMega': 'https://www.micromega.net/feed/',
    'AI4Business': 'https://www.ai4business.it/feed/',
    'Wired Italia': 'https://www.wired.it/feed/rss',
    'ICT Security Magazine': 'https://www.ictsecuritymagazine.com/feed/',
    'Punto Informatico': 'https://www.punto-informatico.it/feed/',
    'Agenda Digitale': 'https://www.agendadigitale.eu/feed/',
    'Il Post': 'https://www.ilpost.it/feed/',
}

# POI: Fonti internazionali (meno notizie, solo top)
INTERNATIONAL_SOURCES = {
    'The Guardian Tech': 'https://www.theguardian.com/technology/rss',
    'MIT Technology Review': 'https://www.technologyreview.com/feed/',
    'The Hacker News': 'https://feeds.feedburner.com/TheHackersNews',
}

all_articles = []
article_id = 1

print("\n📰 FASE 1: FONTI ITALIANE (10 notizie per fonte)")
print("-" * 70)

for source_name, rss_url in ITALIAN_SOURCES.items():
    print(f"\n📡 {source_name}")
    
    try:
        feed = feedparser.parse(rss_url)
        count = 0
        
        for entry in feed.entries[:10]:  # 10 notizie italiane per fonte
            try:
                summary = entry.get('summary', entry.get('description', ''))[:500]
                summary = summary.replace('<p>', '').replace('</p>', '').replace('<br>', ' ')
                summary = summary.replace('&#8217;', "'").replace('&#8220;', '"').replace('&#8221;', '"')
                
                article = {
                    "id": article_id,
                    "title": entry.get('title', '').strip()[:200],
                    "slug": entry.get('title', '').lower().replace(' ', '-').replace("'", '').replace(',', '')[:50],
                    "url": entry.get('link', ''),
                    "summary": summary,
                    "author": entry.get('author', source_name),
                    "published_at": datetime.now().isoformat(),
                    "collected_at": datetime.now().isoformat(),
                    "source_id": 1,
                    "is_featured": count < 2,  # Prime 2 = featured
                    "is_verified": True,
                    "is_archived": False,
                    "quality_score": 0.75 + (0.03 * count),
                    "reading_time_minutes": 3 + (count // 2),
                    "keywords": ["italia", "news", source_name.lower().replace(' ', '-')],
                    "language": "it"
                }
                
                # Cerca immagine
                if hasattr(entry, 'media_content') and entry.media_content:
                    article['image_url'] = entry.media_content[0].get('url')
                elif hasattr(entry, 'enclosures') and entry.enclosures:
                    article['image_url'] = entry.enclosures[0].get('href')
                
                all_articles.append(article)
                print(f"   ✅ {article['title'][:65]}...")
                
                article_id += 1
                count += 1
                
            except Exception as e:
                continue
        
        print(f"   📊 Raccolte: {count} notizie italiane")
        
    except Exception as e:
        print(f"   ❌ Errore: {e}")

print(f"\n📰 FASE 2: FONTI INTERNAZIONALI (3 notizie per fonte - solo top)")
print("-" * 70)

for source_name, rss_url in INTERNATIONAL_SOURCES.items():
    print(f"\n📡 {source_name}")
    
    try:
        feed = feedparser.parse(rss_url)
        count = 0
        
        for entry in feed.entries[:3]:  # Solo 3 migliori
            try:
                summary = entry.get('summary', entry.get('description', ''))[:500]
                summary = summary.replace('<p>', '').replace('</p>', '').replace('<br>', ' ')
                
                article = {
                    "id": article_id,
                    "title": entry.get('title', '').strip()[:200],
                    "slug": entry.get('title', '').lower().replace(' ', '-').replace("'", '')[:50],
                    "url": entry.get('link', ''),
                    "summary": summary,
                    "author": entry.get('author', source_name),
                    "published_at": datetime.now().isoformat(),
                    "collected_at": datetime.now().isoformat(),
                    "source_id": 1,
                    "is_featured": count == 0,  # Solo prima = featured
                    "is_verified": True,
                    "is_archived": False,
                    "quality_score": 0.85 + (0.03 * count),
                    "reading_time_minutes": 4 + count,
                    "keywords": ["international", source_name.lower().replace(' ', '-')],
                    "language": "en"
                }
                
                if hasattr(entry, 'media_content') and entry.media_content:
                    article['image_url'] = entry.media_content[0].get('url')
                
                all_articles.append(article)
                print(f"   ✅ {article['title'][:65]}...")
                
                article_id += 1
                count += 1
                
            except:
                continue
        
        print(f"   📊 Raccolte: {count} notizie internazionali")
        
    except Exception as e:
        print(f"   ❌ Errore: {e}")

print("\n" + "=" * 70)
print(f"🎉 TOTALE: {len(all_articles)} notizie")

italian = len([a for a in all_articles if a['language'] == 'it'])
english = len([a for a in all_articles if a['language'] == 'en'])

print(f"\n📊 BREAKDOWN:")
print(f"   🇮🇹 Italiano: {italian} notizie ({italian/(italian+english)*100:.0f}%)")
print(f"   🇬🇧 Inglese: {english} notizie ({english/(italian+english)*100:.0f}%)")
print(f"\n✅ Priorità alle fonti italiane!")

# Salva
with open('italian_priority_news.json', 'w', encoding='utf-8') as f:
    json.dump({
        "items": all_articles,
        "total": len(all_articles),
        "page": 1,
        "size": 100,
        "pages": 1
    }, f, indent=2, ensure_ascii=False)

print(f"\n💾 Salvate in: italian_priority_news.json")
print(f"🇮🇹 Pronto per app in italiano!")

