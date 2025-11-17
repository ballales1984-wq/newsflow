"""Script per migliorare l'estrazione immagini dagli articoli"""
import json
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin, urlparse
import time

def extract_image_from_webpage(url):
    """Estrae immagine da una pagina web usando Open Graph, meta tags, ecc."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, timeout=10, headers=headers, allow_redirects=True)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 1. Open Graph image (priorità alta)
        og_image = soup.find('meta', property='og:image')
        if og_image and og_image.get('content'):
            img_url = og_image.get('content')
            if img_url.startswith('//'):
                img_url = 'https:' + img_url
            elif img_url.startswith('/'):
                img_url = urljoin(url, img_url)
            if img_url.startswith('http'):
                return img_url
        
        # 2. Twitter card image
        twitter_image = soup.find('meta', attrs={'name': 'twitter:image'})
        if twitter_image and twitter_image.get('content'):
            img_url = twitter_image.get('content')
            if img_url.startswith('//'):
                img_url = 'https:' + img_url
            elif img_url.startswith('/'):
                img_url = urljoin(url, img_url)
            if img_url.startswith('http'):
                return img_url
        
        # 3. Prima immagine <img> nel contenuto principale
        # Cerca in article, main, o body
        content_areas = soup.find_all(['article', 'main', 'div'], class_=re.compile(r'content|article|post|entry', re.I))
        if not content_areas:
            content_areas = [soup.find('body')]
        
        for area in content_areas:
            if area:
                img = area.find('img', src=True)
                if img:
                    img_url = img.get('src')
                    if img_url.startswith('//'):
                        img_url = 'https:' + img_url
                    elif img_url.startswith('/'):
                        img_url = urljoin(url, img_url)
                    if img_url.startswith('http') and not any(x in img_url.lower() for x in ['logo', 'icon', 'avatar', 'button']):
                        return img_url
        
        # 4. Qualsiasi immagine grande nel body
        images = soup.find_all('img', src=True)
        for img in images:
            img_url = img.get('src')
            width = img.get('width', '0')
            height = img.get('height', '0')
            
            # Preferisci immagini grandi (probabilmente contenuto, non logo)
            try:
                w = int(width) if width.isdigit() else 0
                h = int(height) if height.isdigit() else 0
                if w > 300 or h > 300:  # Immagine abbastanza grande
                    if img_url.startswith('//'):
                        img_url = 'https:' + img_url
                    elif img_url.startswith('/'):
                        img_url = urljoin(url, img_url)
                    if img_url.startswith('http') and not any(x in img_url.lower() for x in ['logo', 'icon', 'avatar']):
                        return img_url
            except:
                pass
        
    except Exception as e:
        return None
    
    return None

def migliora_immagini_json(input_file, output_file=None, max_articles=None):
    """Migliora le immagini nel file JSON"""
    if output_file is None:
        output_file = input_file
    
    print(f"📖 Leggendo {input_file}...")
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    articles = data.get('items', [])
    print(f"📰 Trovati {len(articles)} articoli")
    
    if max_articles:
        articles_to_process = articles[:max_articles]
        print(f"🔍 Processando solo i primi {max_articles} articoli (test)")
    else:
        articles_to_process = articles
    
    fixed_count = 0
    skipped_count = 0
    
    for i, article in enumerate(articles_to_process, 1):
        # Se già ha immagine, salta
        if article.get('image_url'):
            skipped_count += 1
            continue
        
        url = article.get('url', '')
        if not url:
            continue
        
        print(f"\n[{i}/{len(articles_to_process)}] {article.get('title', '')[:60]}...")
        print(f"   🔍 Cercando immagine in: {url[:60]}...")
        
        image_url = extract_image_from_webpage(url)
        
        if image_url:
            article['image_url'] = image_url
            fixed_count += 1
            print(f"   ✅ Immagine trovata: {image_url[:80]}...")
        else:
            print(f"   ❌ Nessuna immagine trovata")
        
        # Rate limiting per non sovraccaricare i server
        time.sleep(1)
    
    print(f"\n✨ Risultati:")
    print(f"   ✅ Immagini aggiunte: {fixed_count}")
    print(f"   ⏭️  Saltati (già con immagine): {skipped_count}")
    print(f"   ❌ Senza immagine: {len(articles_to_process) - fixed_count - skipped_count}")
    
    print(f"\n💾 Salvando in {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print("✅ Completato!")
    return fixed_count

if __name__ == '__main__':
    import sys
    
    print("🖼️  Miglioramento estrazione immagini da pagine web")
    print("=" * 70)
    
    # Test con primi 10 articoli
    test_mode = '--test' in sys.argv
    
    backend_file = 'final_news_italian.json'
    
    if test_mode:
        print("\n🧪 MODALITÀ TEST: processerà solo i primi 10 articoli")
        migliora_immagini_json(backend_file, max_articles=10)
    else:
        print("\n🚀 MODALITÀ COMPLETA: processerà tutti gli articoli")
        print("⏳ Questo richiederà alcuni minuti...")
        migliora_immagini_json(backend_file)

