"""Verifica immagini nel JSON"""
import json

with open('final_news_italian.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

items = data.get('items', [])
with_img = [item for item in items if item.get('image_url')]
without_img = [item for item in items if not item.get('image_url')]

print(f'📊 Analisi immagini:')
print(f'   Total articoli: {len(items)}')
print(f'   Con image_url: {len(with_img)}')
print(f'   Senza image_url: {len(without_img)}')
print(f'   Percentuale: {len(with_img)/len(items)*100:.1f}%')
print('')

if with_img:
    print('🖼️  Esempi articoli CON immagini:')
    for i, item in enumerate(with_img[:5], 1):
        print(f'   {i}. {item.get("title", "N/A")[:60]}...')
        print(f'      URL: {item.get("image_url", "N/A")[:100]}...')
        print('')
else:
    print('❌ Nessun articolo con immagini!')

if without_img:
    print('📝 Esempi articoli SENZA immagini:')
    for i, item in enumerate(without_img[:3], 1):
        print(f'   {i}. {item.get("title", "N/A")[:60]}...')
        print(f'      Summary: {item.get("summary", "N/A")[:100]}...')
        print('')
