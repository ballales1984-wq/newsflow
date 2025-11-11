"""Raccolta completa da TUTTE le fonti autorevoli"""
import feedparser
import json
from datetime import datetime

print("🌍 Raccogliendo notizie da TUTTE le fonti autorevoli...")
print("=" * 70)

# Fonti complete come richiesto nel progetto originale
RSS_SOURCES = {
    # Tecnologia Internazionale
    'MIT Technology Review': 'https://www.technologyreview.com/feed/',
    'The Guardian Tech': 'https://www.theguardian.com/technology/rss',
    'Wired IT': 'https://www.wired.it/feed/rss',
    'The Hacker News': 'https://feeds.feedburner.com/TheHackersNews',
    
    # Italia - Qualità
    'MicroMega': 'https://www.micromega.net/feed/',
    'AI4Business': 'https://www.ai4business.it/feed/',
    'ICT Security Magazine': 'https://www.ictsecuritymagazine.com/feed/',
    'Punto Informatico': 'https://www.punto-informatico.it/feed/',
    'Agenda Digitale': 'https://www.agendadigitale.eu/feed/',
    
    # Scienza
    'ArXiv CS': 'http://export.arxiv.org/rss/cs',
}

all_articles = []
article_id = 1
source_id = 1

for source_name, rss_url in RSS_SOURCES.items():
    print(f"\n📡 {source_name}")
    print(f"   {rss_url}")
    
    try:
        feed = feedparser.parse(rss_url)
        
        if feed.bozo:
            print(f"   ⚠️  Feed ha warning (ma procedo)")
        
        count = 0
        for entry in feed.entries[:5]:  # 5 notizie per fonte = 50 totali
            try:
                # Pulizia summary (rimuovi HTML)
                summary = entry.get('summary', entry.get('description', ''))[:400]
                summary = summary.replace('<p>', '').replace('</p>', '').replace('<br>', ' ')
                
                # Determina lingua
                language = 'it' if source_name in ['MicroMega', 'AI4Business', 'ICT Security Magazine', 
                                                     'Punto Informatico', 'Agenda Digitale', 'Wired IT'] else 'en'
                
                # Determina categoria
                if 'Security' in source_name or 'Hacker' in source_name:
                    category = 'Cybersecurity'
                elif 'ArXiv' in source_name:
                    category = 'Science'
                elif 'MicroMega' in source_name:
                    category = 'Philosophy'
                else:
                    category = 'Technology'
                
                article = {
                    "id": article_id,
                    "title": entry.get('title', '').strip()[:200],
                    "slug": entry.get('title', '').lower().replace(' ', '-').replace("'", '')[:50],
                    "url": entry.get('link', ''),
                    "summary": summary,
                    "content": entry.get('content', [{}])[0].get('value', summary) if 'content' in entry else summary,
                    "author": entry.get('author', source_name),
                    "published_at": datetime.now().isoformat(),
                    "collected_at": datetime.now().isoformat(),
                    "source_id": source_id,
                    "category_id": None,
                    "is_featured": count == 0 and source_id <= 3,  # Prime 3 fonti = featured
                    "is_verified": True,
                    "is_archived": False,
                    "quality_score": 0.7 + (0.05 * (5 - count)),
                    "reading_time_minutes": 3 + count,
                    "keywords": [category.lower(), "news", language],
                    "language": language,
                    "image_url": None
                }
                
                # Cerca immagine
                if hasattr(entry, 'media_content') and entry.media_content:
                    article['image_url'] = entry.media_content[0].get('url')
                elif hasattr(entry, 'media_thumbnail') and entry.media_thumbnail:
                    article['image_url'] = entry.media_thumbnail[0].get('url')
                
                all_articles.append(article)
                print(f"   ✅ [{category}] {article['title'][:60]}...")
                
                article_id += 1
                count += 1
                
            except Exception as e:
                print(f"   ⚠️  Errore entry: {e}")
                continue
        
        print(f"   📊 Raccolte: {count} notizie")
        source_id += 1
        
    except Exception as e:
        print(f"   ❌ Errore fonte: {e}")

print("\n" + "=" * 70)
print(f"🎉 TOTALE: {len(all_articles)} notizie raccolte da {len(RSS_SOURCES)} fonti!")
print(f"📊 Breakdown:")
print(f"   - Tecnologia: {len([a for a in all_articles if 'technology' in a['keywords']])} notizie")
print(f"   - Cybersecurity: {len([a for a in all_articles if 'cybersecurity' in a['keywords']])} notizie")
print(f"   - Scienza: {len([a for a in all_articles if 'science' in a['keywords']])} notizie")
print(f"   - Filosofia: {len([a for a in all_articles if 'philosophy' in a['keywords']])} notizie")
print(f"   - Italiano: {len([a for a in all_articles if a['language'] == 'it'])} notizie")
print(f"   - Inglese: {len([a for a in all_articles if a['language'] == 'en'])} notizie")

# Salva
with open('all_sources_news.json', 'w', encoding='utf-8') as f:
    json.dump({
        "items": all_articles,
        "total": len(all_articles),
        "page": 1,
        "size": 50,
        "pages": 1
    }, f, indent=2, ensure_ascii=False)

print(f"\n💾 Salvate in: all_sources_news.json")
print(f"✅ Pronto per aggiornare l'app!")

