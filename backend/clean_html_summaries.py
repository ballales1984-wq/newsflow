"""Pulisce i tag HTML dai sommari delle notizie"""
import json
import re
from bs4 import BeautifulSoup

print("🧹 Pulizia HTML dai sommari...")

# Carica notizie
with open('final_news_italian.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    articles = data['items']

def clean_html(text):
    """Rimuove tutti i tag HTML e lascia solo testo pulito"""
    if not text:
        return text
    
    # Usa BeautifulSoup per rimuovere HTML
    soup = BeautifulSoup(text, 'html.parser')
    clean_text = soup.get_text()
    
    # Pulisci spazi multipli
    clean_text = re.sub(r'\s+', ' ', clean_text)
    
    # Rimuovi caratteri speciali HTML
    clean_text = clean_text.replace('&nbsp;', ' ')
    clean_text = clean_text.replace('&#8217;', "'")
    clean_text = clean_text.replace('&#8220;', '"')
    clean_text = clean_text.replace('&#8221;', '"')
    clean_text = clean_text.replace('&#8230;', '...')
    
    return clean_text.strip()

# Pulisci tutti i sommari
cleaned = 0
for article in articles:
    original_summary = article.get('summary', '')
    
    if '<' in original_summary or '&' in original_summary:
        article['summary'] = clean_html(original_summary)
        cleaned += 1
        print(f"✅ Pulito: {article['title'][:60]}...")

print(f"\n📊 Puliti {cleaned}/{len(articles)} sommari")

# Salva
with open('final_news_italian.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"💾 Salvato in: final_news_italian.json")
print(f"✅ Sommari puliti e pronti!")

