"""Verifica immagini nel JSON"""
import json

with open('final_news_italian.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

items = data.get('items', [])
with_img = [item for item in items if item.get('image_url')]

print(f'📊 Analisi immagini:')
print(f'   Total articoli: {len(items)}')
print(f'   Con image_url: {len(with_img)}')
print(f'   Senza image_url: {len(items) - len(with_img)}')
print('')

if with_img:
    print('🖼️  Esempi immagini trovate:')
    for i, item in enumerate(with_img[:5], 1):
        print(f'   {i}. {item.get("title", "N/A")[:50]}...')
        print(f'      URL: {item.get("image_url", "N/A")[:80]}...')
        print('')
else:
    print('❌ Nessuna immagine trovata nel JSON!')
    print('')
    print('📝 Verifica primi 3 articoli:')
    for i, item in enumerate(items[:3], 1):
        print(f'   {i}. {item.get("title", "N/A")[:50]}...')
        print(f'      image_url: {item.get("image_url", "NON PRESENTE")}')
        print(f'      summary length: {len(item.get("summary", ""))}')
        print('')

