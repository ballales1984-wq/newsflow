"""Script per generare il digest giornaliero dai nuovi articoli"""
import json
import os
from datetime import datetime
from collections import defaultdict

# Mappa category_id -> nome categoria
CATEGORY_MAP = {
    1: "Tecnologia",
    2: "Scienza",
    3: "Filosofia",
    4: "Cybersecurity",
    5: "Intelligenza Artificiale",
    6: "Innovazione",
    7: "Cultura",
    8: "Etica",
    9: "Sport",
    10: "Natura & Ambiente",
    11: "Business & Economia",
    12: "Salute",
    13: "Politica",
    14: "Intrattenimento"
}

# Emoji per categoria
CATEGORY_EMOJI = {
    1: "💻",
    2: "🔬",
    3: "🤔",
    4: "🔒",
    5: "🤖",
    6: "💡",
    7: "🎨",
    8: "⚖️",
    9: "⚽",
    10: "🌍",
    11: "💼",
    12: "🏥",
    13: "🏛️",
    14: "🎬"
}

def load_articles():
    """Carica gli articoli dal file JSON"""
    possible_paths = [
        'final_news_italian.json',
        os.path.join('backend', 'final_news_italian.json'),
        os.path.join('api', 'final_news_italian.json')
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('items', [])
    
    return []

def generate_digest():
    """Genera il digest giornaliero dagli articoli"""
    articles = load_articles()
    
    if not articles:
        print("❌ Nessun articolo trovato!")
        return None
    
    print(f"📚 Caricati {len(articles)} articoli")
    
    # Raggruppa articoli per categoria
    articles_by_category = defaultdict(list)
    
    for article in articles:
        category_id = article.get('category_id', 1)
        category_name = CATEGORY_MAP.get(category_id, "Tecnologia")
        
        # Prendi solo i primi 5 articoli per categoria (i più recenti/importanti)
        if len(articles_by_category[category_id]) < 5:
            articles_by_category[category_id].append({
                'title': article.get('title', ''),
                'description': article.get('summary', '')[:200]  # Primi 200 caratteri
            })
    
    # Costruisci il digest
    digest_categories = []
    
    for category_id in sorted(articles_by_category.keys()):
        category_name = CATEGORY_MAP.get(category_id, "Tecnologia")
        emoji = CATEGORY_EMOJI.get(category_id, "📰")
        
        if articles_by_category[category_id]:
            digest_categories.append({
                'category': f"{emoji} {category_name}",
                'articles': articles_by_category[category_id]
            })
    
    # Data di oggi
    today = datetime.now().strftime("%Y-%m-%d")
    
    digest_data = {
        'date': today,
        'digest': digest_categories
    }
    
    return digest_data

def save_digest(digest_data):
    """Salva il digest in tutti i path necessari"""
    if not digest_data:
        return
    
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Path da salvare
    paths_to_save = [
        'backend/digest.json',
        'api/digest.json',
        'frontend/src/assets/digest.json'
    ]
    
    saved_count = 0
    for path in paths_to_save:
        try:
            # Crea directory se non esiste
            os.makedirs(os.path.dirname(path), exist_ok=True)
            
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(digest_data, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Digest salvato in: {path}")
            saved_count += 1
        except Exception as e:
            print(f"⚠️  Errore salvataggio {path}: {e}")
    
    print(f"\n✨ Digest salvato in {saved_count} posizioni!")
    print(f"📅 Data: {today}")
    print(f"📊 Categorie: {len(digest_data['digest'])}")
    
    total_articles = sum(len(cat['articles']) for cat in digest_data['digest'])
    print(f"📰 Articoli totali: {total_articles}")

if __name__ == '__main__':
    print("=" * 70)
    print("GENERAZIONE DIGEST GIORNALIERO")
    print("=" * 70)
    
    digest = generate_digest()
    
    if digest:
        save_digest(digest)
        print("\n✅ Digest generato con successo!")
    else:
        print("\n❌ Errore nella generazione del digest")

