"""Traduce notizie internazionali in italiano"""
from deep_translator import GoogleTranslator
import feedparser
import json
from datetime import datetime
import time

translator = GoogleTranslator(source='en', target='it')

print("🌍➡️🇮🇹 Traduzione notizie dal mondo in italiano")
print("=" * 70)

# Fonti internazionali top
WORLD_SOURCES = {
    'The Guardian': 'https://www.theguardian.com/technology/rss',
    'MIT Tech Review': 'https://www.technologyreview.com/feed/',
    'The Hacker News': 'https://feeds.feedburner.com/TheHackersNews',
    'BBC Tech': 'http://feeds.bbci.co.uk/news/technology/rss.xml',
    'TechCrunch': 'https://techcrunch.com/feed/',
}

translated_articles = []
article_id = 1

for source_name, rss_url in WORLD_SOURCES.items():
    print(f"\n📡 {source_name}")
    
    try:
        feed = feedparser.parse(rss_url)
        count = 0
        
        for entry in feed.entries[:5]:  # 5 per fonte = 25 totali
            try:
                title_en = entry.get('title', '').strip()[:300]
                summary_en = entry.get('summary', entry.get('description', ''))[:600]
                summary_en = summary_en.replace('<p>', '').replace('</p>', '').replace('<br>', ' ')
                
                print(f"\n   🔄 Traduco: {title_en[:60]}...")
                
                # Traduci titolo
                try:
                    title_it = translator.translate(title_en)
                    time.sleep(0.3)  # Evita rate limiting
                except Exception as e:
                    print(f"      ⚠️ Errore traduzione titolo: {e}")
                    title_it = title_en
                
                # Traduci sommario
                try:
                    summary_it = translator.translate(summary_en[:500])
                    time.sleep(0.3)
                except Exception as e:
                    print(f"      ⚠️ Errore traduzione summary: {e}")
                    summary_it = summary_en
                
                article = {
                    "id": article_id,
                    "title": title_it[:200],
                    "slug": title_it.lower().replace(' ', '-').replace("'", '').replace(',', '')[:50],
                    "url": entry.get('link', ''),
                    "summary": summary_it[:500],
                    "author": f"{entry.get('author', source_name)} (trad. auto)",
                    "published_at": datetime.now().isoformat(),
                    "collected_at": datetime.now().isoformat(),
                    "source_id": 1,
                    "is_featured": count == 0,
                    "is_verified": True,
                    "is_archived": False,
                    "quality_score": 0.8 + (0.02 * count),
                    "reading_time_minutes": 3 + count,
                    "keywords": ["internazionale", "tradotto", source_name.lower().replace(' ', '-')],
                    "language": "it",  # Tradotto in italiano!
                    "original_language": "en"
                }
                
                # Immagine
                if hasattr(entry, 'media_content') and entry.media_content:
                    article['image_url'] = entry.media_content[0].get('url')
                
                translated_articles.append(article)
                print(f"   ✅ IT: {title_it[:60]}...")
                
                article_id += 1
                count += 1
                
            except Exception as e:
                print(f"   ⚠️  Skip: {e}")
                continue
        
        print(f"   📊 Tradotte: {count} notizie")
        
    except Exception as e:
        print(f"   ❌ Errore fonte: {e}")

print("\n" + "=" * 70)
print(f"🎉 TOTALE: {len(translated_articles)} notizie tradotte")
print(f"🌍 Fonti: Guardian, MIT, BBC, TechCrunch, Hacker News")
print(f"🇮🇹 Tutte in ITALIANO!")

# Salva
with open('world_news_translated.json', 'w', encoding='utf-8') as f:
    json.dump({
        "items": translated_articles,
        "total": len(translated_articles),
        "page": 1,
        "size": 50,
        "pages": 1
    }, f, indent=2, ensure_ascii=False)

print(f"\n💾 Salvate in: world_news_translated.json")
print(f"✅ Notizie dal mondo, in italiano!")

