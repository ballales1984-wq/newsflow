import json
import os

# Carica il file JSON
file_path = 'final_news_italian.json'
if not os.path.exists(file_path):
    file_path = os.path.join('..', 'backend', 'final_news_italian.json')

with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Cerca articoli da Google News
google_news = []
for article in data.get('items', []):
    keywords = ' '.join(article.get('keywords', [])).lower()
    author = str(article.get('author', '')).lower()
    
    if 'google news' in keywords or 'google news' in author:
        google_news.append(article)

print(f"\n📰 Articoli da Google News trovati: {len(google_news)}")
print(f"📊 Totale articoli nel file: {len(data.get('items', []))}")

if google_news:
    print("\n✅ Prime 5 notizie da Google News:")
    for i, article in enumerate(google_news[:5], 1):
        title = article.get('title', 'N/A')[:80]
        author = article.get('author', 'N/A')
        category = article.get('category_id', 'N/A')
        print(f"\n{i}. {title}")
        print(f"   Autore: {author}")
        print(f"   Categoria ID: {category}")
else:
    print("\n⚠️  Nessun articolo da Google News trovato nel file.")
    print("   Questo potrebbe significare che:")
    print("   - La raccolta non ha incluso Google News")
    print("   - Gli articoli non hanno il tag 'google news' nei keywords")

