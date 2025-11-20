"""Script per scaricare e salvare le immagini degli articoli localmente"""
import json
import requests
import os
from pathlib import Path
from urllib.parse import urlparse
import hashlib
import time

def get_image_extension(url):
    """Estrae estensione immagine dall'URL"""
    parsed = urlparse(url)
    path = parsed.path.lower()
    
    # Estensioni comuni
    if path.endswith('.jpg') or path.endswith('.jpeg'):
        return '.jpg'
    elif path.endswith('.png'):
        return '.png'
    elif path.endswith('.gif'):
        return '.gif'
    elif path.endswith('.webp'):
        return '.webp'
    else:
        # Default: jpg
        return '.jpg'

def download_image(image_url, output_path):
    """Scarica immagine da URL e salva in file"""
    if not image_url:
        return False
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(image_url, timeout=15, headers=headers, allow_redirects=True)
        response.raise_for_status()
        
        # Verifica che sia un'immagine
        content_type = response.headers.get('content-type', '').lower()
        if not content_type.startswith('image/'):
            print(f"   ⚠️  URL non è un'immagine: {content_type}")
            return False
        
        # Crea directory se non esiste
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Salva immagine
        with open(output_path, 'wb') as f:
            f.write(response.content)
        
        return True
    except Exception as e:
        print(f"   ❌ Errore download: {e}")
        return False

def process_articles_json(input_file, output_file=None, images_dir=None):
    """Processa articoli JSON: scarica immagini e aggiorna percorsi"""
    if output_file is None:
        output_file = input_file
    
    # Determina directory immagini
    if images_dir is None:
        # Trova root del progetto (backend -> root)
        backend_dir = Path(__file__).parent
        root_dir = backend_dir.parent
        images_dir = root_dir / 'frontend' / 'src' / 'assets' / 'images'
    else:
        images_dir = Path(images_dir)
    
    # Crea directory immagini se non esiste
    images_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"📖 Leggendo {input_file}...")
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    articles = data.get('items', [])
    print(f"📰 Trovati {len(articles)} articoli")
    print(f"📁 Directory immagini: {images_dir}")
    print("")
    
    downloaded_count = 0
    skipped_count = 0
    error_count = 0
    
    for i, article in enumerate(articles, 1):
        image_url = article.get('image_url')
        
        # Se non ha immagine, salta
        if not image_url:
            skipped_count += 1
            continue
        
        # Se già ha percorso locale, salta
        if image_url.startswith('/assets/') or image_url.startswith('assets/'):
            skipped_count += 1
            continue
        
        print(f"[{i}/{len(articles)}] {article.get('title', '')[:60]}...")
        print(f"   🔗 URL: {image_url[:80]}...")
        
        # Genera nome file univoco basato su hash dell'URL
        url_hash = hashlib.md5(image_url.encode()).hexdigest()[:12]
        ext = get_image_extension(image_url)
        image_filename = f"{url_hash}{ext}"
        image_path = images_dir / image_filename
        
        # Se immagine già esiste, usa quella
        if image_path.exists():
            print(f"   ✅ Immagine già esistente: {image_filename}")
            article['image_url'] = f'/assets/images/{image_filename}'
            downloaded_count += 1
        else:
            # Scarica immagine
            print(f"   ⬇️  Scaricando...")
            if download_image(image_url, image_path):
                print(f"   ✅ Salvata: {image_filename}")
                article['image_url'] = f'/assets/images/{image_filename}'
                downloaded_count += 1
                
                # Rate limiting
                time.sleep(0.5)
            else:
                print(f"   ❌ Fallito download")
                error_count += 1
        
        print("")
    
    print(f"\n✨ Risultati:")
    print(f"   ✅ Immagini scaricate/esistenti: {downloaded_count}")
    print(f"   ⏭️  Saltati (senza immagine o già locale): {skipped_count}")
    print(f"   ❌ Errori: {error_count}")
    
    print(f"\n💾 Salvando JSON aggiornato in {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print("✅ Completato!")
    return downloaded_count

if __name__ == '__main__':
    import sys
    
    print("🖼️  Download e salvataggio immagini articoli")
    print("=" * 70)
    
    # File da processare
    backend_file = 'final_news_italian.json'
    
    if len(sys.argv) > 1:
        backend_file = sys.argv[1]
    
    if not os.path.exists(backend_file):
        print(f"❌ File non trovato: {backend_file}")
        sys.exit(1)
    
    print(f"\n📁 File input: {backend_file}")
    print(f"📁 File output: {backend_file} (sovrascritto)")
    print(f"📁 Directory immagini: frontend/src/assets/images/")
    print("")
    
    process_articles_json(backend_file)

