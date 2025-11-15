"""Script per generare il digest giornaliero dai nuovi articoli"""
import json
import os
from datetime import datetime, timedelta
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
    """Genera il digest giornaliero dagli articoli - SOLO NOTIZIE DI OGGI"""
    articles = load_articles()
    
    if not articles:
        print("❌ Nessun articolo trovato!")
        return None
    
        print(f"Caricati {len(articles)} articoli totali")
    
    # Filtra solo articoli di oggi (ultime 24h)
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    today_articles = []
    
    for article in articles:
        published_at = article.get('published_at', '')
        if not published_at:
            continue
        
        try:
            # Prova a parsare la data in vari formati
            if isinstance(published_at, str):
                article_date = None
                
                # Prova formato ISO: "2025-11-15T10:04:00"
                if 'T' in published_at:
                    date_str = published_at.split('T')[0]
                    try:
                        article_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                    except:
                        pass
                
                # Prova formato US: "11/15/2025 10:04:00"
                if not article_date and '/' in published_at:
                    date_str = published_at.split(' ')[0]  # Prende "11/15/2025"
                    try:
                        article_date = datetime.strptime(date_str, '%m/%d/%Y').date()
                    except:
                        pass
                
                # Prova formato standard: "2025-11-15"
                if not article_date:
                    date_str = published_at.split(' ')[0]
                    try:
                        article_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                    except:
                        pass
                
                if article_date:
                    # Filtra solo articoli di oggi o ieri (ultime 24h)
                    if article_date >= yesterday:
                        today_articles.append(article)
        except Exception as e:
            # Se non riesce a parsare, salta l'articolo
            continue
    
    print(f"📅 Articoli di oggi/ultime 24h: {len(today_articles)}")
    
    if not today_articles:
        print("⚠️  Nessun articolo di oggi trovato!")
        return None
    
    # Ordina per data (più recenti prima)
    today_articles.sort(key=lambda x: x.get('published_at', ''), reverse=True)
    
    # Raggruppa articoli per categoria
    articles_by_category = defaultdict(list)
    
    for article in today_articles:
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

