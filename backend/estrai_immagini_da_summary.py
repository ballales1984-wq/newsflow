"""Script per estrarre immagini dal summary HTML degli articoli esistenti"""
import json
import re
from pathlib import Path

def extract_image_from_html(html_content):
    """Estrae l'URL della prima immagine trovata nell'HTML"""
    if not html_content:
        return None
    
    # Cerca tag <img> con src
    img_match = re.search(r'<img[^>]+src=["\']([^"\']+)["\']', html_content, re.IGNORECASE)
    if img_match:
        return img_match.group(1)
    
    # Cerca anche con attributi diversi
    img_match = re.search(r'<img[^>]+src=([^\s>]+)', html_content, re.IGNORECASE)
    if img_match:
        url = img_match.group(1).strip('"\'')
        return url
    
    return None

def fix_images_in_json(input_file, output_file=None):
    """Corregge le immagini mancanti nel file JSON"""
    if output_file is None:
        output_file = input_file
    
    print(f"📖 Leggendo {input_file}...")
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    articles = data.get('items', [])
    print(f"📰 Trovati {len(articles)} articoli")
    
    fixed_count = 0
    for article in articles:
        # Se l'articolo non ha image_url o è null
        if not article.get('image_url'):
            # Cerca nel summary
            summary = article.get('summary', '')
            image_url = extract_image_from_html(summary)
            
            # Se non trovato, cerca anche nel content
            if not image_url:
                content = article.get('content', '')
                if isinstance(content, str):
                    image_url = extract_image_from_html(content)
            
            if image_url:
                article['image_url'] = image_url
                fixed_count += 1
                print(f"   ✅ Immagine estratta: {article.get('title', '')[:60]}...")
                print(f"      URL: {image_url[:80]}...")
    
    print(f"\n✨ Corrette {fixed_count} immagini su {len(articles)} articoli")
    
    print(f"💾 Salvando in {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print("✅ Completato!")
    return fixed_count

if __name__ == '__main__':
    # File da processare
    input_file = Path(__file__).parent / 'italian_priority_news.json'
    frontend_file = Path(__file__).parent.parent / 'frontend' / 'src' / 'assets' / 'final_news_italian.json'
    
    print("🖼️  Estrazione immagini da summary HTML")
    print("=" * 70)
    
    # Processa il file del backend
    if input_file.exists():
        print("\n1️⃣  Processando file backend...")
        fix_images_in_json(str(input_file))
    else:
        print(f"⚠️  File backend non trovato: {input_file}")
    
    # Processa il file del frontend
    if frontend_file.exists():
        print("\n2️⃣  Processando file frontend...")
        fix_images_in_json(str(frontend_file))
    else:
        print(f"⚠️  File frontend non trovato: {frontend_file}")

