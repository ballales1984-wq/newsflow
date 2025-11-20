"""Raccolta notizie con PRIORITÀ alle fonti ITALIANE"""
import feedparser
import json
import re
import requests
import os
from datetime import datetime

print("🇮🇹 Raccogliendo notizie - PRIORITÀ ITALIANE")
print("=" * 70)

# STEP 0: Carica PRIMA le notizie vecchie (se esistono) per mantenerle durante l'aggiornamento
print("\n📰 STEP 0: Caricamento notizie vecchie (se esistono)...")
old_articles = []
old_file_path = 'final_news_italian.json'
if os.path.exists(old_file_path):
    try:
        with open(old_file_path, 'r', encoding='utf-8') as f:
            old_data = json.load(f)
            old_articles = old_data.get('items', [])
            print(f"   ✅ Caricate {len(old_articles)} notizie vecchie (verranno sostituite con le nuove)")
    except Exception as e:
        print(f"   ⚠️  Errore caricamento notizie vecchie: {e}")
else:
    print(f"   ℹ️  Nessun file vecchio trovato - prima raccolta")

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
        # Usa requests con timeout per evitare blocchi
        try:
            response = requests.get(rss_url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
            response.raise_for_status()
            feed = feedparser.parse(response.content)
        except requests.exceptions.Timeout:
            print(f"   ⚠️  Timeout (10s) - salto questa fonte")
            continue
        except requests.exceptions.RequestException as e:
            print(f"   ⚠️  Errore richiesta: {e} - salto questa fonte")
            continue
        
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
                
                # Cerca immagine - metodi multipli
                image_url = None
                
                # Metodo 1: media_content
                if hasattr(entry, 'media_content') and entry.media_content:
                    image_url = entry.media_content[0].get('url')
                
                # Metodo 2: enclosures
                if not image_url and hasattr(entry, 'enclosures') and entry.enclosures:
                    image_url = entry.enclosures[0].get('href')
                
                # Metodo 3: estrai da HTML summary/description
                if not image_url:
                    full_content = entry.get('summary', entry.get('description', ''))
                    # Cerca tag <img> con src (pattern più robusto)
                    img_match = re.search(r'<img[^>]+src=["\']([^"\']+)["\']', full_content, re.IGNORECASE)
                    if img_match:
                        image_url = img_match.group(1)
                    # Pattern alternativo senza virgolette
                    if not image_url:
                        img_match = re.search(r'<img[^>]+src=([^\s>]+)', full_content, re.IGNORECASE)
                        if img_match:
                            image_url = img_match.group(1).strip('"\'')
                    # Cerca anche nel campo article['summary'] già salvato
                    if not image_url and article.get('summary'):
                        img_match = re.search(r'<img[^>]+src=["\']([^"\']+)["\']', article['summary'], re.IGNORECASE)
                        if img_match:
                            image_url = img_match.group(1)
                    # Cerca anche in content se disponibile
                    if not image_url and hasattr(entry, 'content'):
                        for content_item in entry.content:
                            content_text = content_item.get('value', '')
                            img_match = re.search(r'<img[^>]+src=["\']([^"\']+)["\']', content_text, re.IGNORECASE)
                            if img_match:
                                image_url = img_match.group(1)
                                break
                
                # Metodo 4: links con type image
                if not image_url and hasattr(entry, 'links'):
                    for link in entry.links:
                        if link.get('type', '').startswith('image/'):
                            image_url = link.get('href')
                            break
                
                article['image_url'] = image_url if image_url else None
                
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
        # Usa requests con timeout per evitare blocchi
        try:
            response = requests.get(rss_url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
            response.raise_for_status()
            feed = feedparser.parse(response.content)
        except requests.exceptions.Timeout:
            print(f"   ⚠️  Timeout (10s) - salto questa fonte")
            continue
        except requests.exceptions.RequestException as e:
            print(f"   ⚠️  Errore richiesta: {e} - salto questa fonte")
            continue
        
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
                
                # Cerca immagine - metodi multipli
                image_url = None
                
                # Metodo 1: media_content
                if hasattr(entry, 'media_content') and entry.media_content:
                    image_url = entry.media_content[0].get('url')
                
                # Metodo 2: estrai da HTML summary/description
                if not image_url:
                    full_content = entry.get('summary', entry.get('description', ''))
                    img_match = re.search(r'<img[^>]+src=["\']([^"\']+)["\']', full_content, re.IGNORECASE)
                    if img_match:
                        image_url = img_match.group(1)
                
                # Metodo 3: links con type image
                if not image_url and hasattr(entry, 'links'):
                    for link in entry.links:
                        if link.get('type', '').startswith('image/'):
                            image_url = link.get('href')
                            break
                
                article['image_url'] = image_url if image_url else None
                
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

