"""Versione semplificata di main.py per deploy veloce senza dipendenze complesse"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import os
import json
from app.core.auth_fingerprint import FingerprintAuth

# Create FastAPI app
app = FastAPI(
    title="NewsFlow",
    version="1.0.0",
    description="Intelligent News Curation Platform"
)

# Configure CORS
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:4200").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    """Root endpoint"""
    return {
        "name": "NewsFlow",
        "version": "1.0.0",
        "status": "running",
        "message": "Backend is alive! 🚀"
    }


@app.get("/api/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


def _load_articles():
    """Helper to load articles - 94 NEWS ALL IN ITALIAN"""
    import json
    import os
    import re
    
    def clean_html(text):
        """Rimuove tutti i tag HTML dal testo"""
        if not text:
            return ""
        import html
        # Rimuove tutti i tag HTML
        text = re.sub(r'<[^>]+>', '', text)
        # Decodifica entità HTML (inclusi quelli numerici come &#8217;)
        try:
            text = html.unescape(text)
        except:
            # Fallback manuale se html.unescape non disponibile
            text = text.replace('&nbsp;', ' ')
            text = text.replace('&amp;', '&')
            text = text.replace('&lt;', '<')
            text = text.replace('&gt;', '>')
            text = text.replace('&quot;', '"')
            text = text.replace('&#39;', "'")
            text = text.replace('&apos;', "'")
            # Decodifica entità numeriche comuni
            text = text.replace('&#8217;', "'")  # apostrofo
            text = text.replace('&#8216;', "'")  # apostrofo sinistro
            text = text.replace('&#8220;', '"')  # virgolette sinistre
            text = text.replace('&#8221;', '"')  # virgolette destre
            text = text.replace('&#8230;', '...')  # tre puntini
            text = text.replace('&mdash;', '—')  # dash
            text = text.replace('&ndash;', '–')  # en dash
        # Rimuove spazi multipli
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    # Determina il path base (directory corrente o backend/)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Torna alla root backend
    if not os.path.exists(os.path.join(base_dir, 'final_news_italian.json')):
        # Se non trovato, prova directory corrente
        base_dir = os.getcwd()
    
    # Usa il file finale con tutte le notizie in italiano
    file_path = os.path.join(base_dir, 'final_news_italian.json')
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                articles = data.get('items', [])
                # Pulisce HTML da tutte le notizie esistenti
                for article in articles:
                    if 'summary' in article:
                        article['summary'] = clean_html(article['summary'])
                    if 'title' in article:
                        article['title'] = clean_html(article['title'])
                return articles
        except Exception as e:
            print(f"Errore caricamento final_news_italian.json: {e}")
            pass
    
    # Fallback su tutte le fonti
    file_path = os.path.join(base_dir, 'all_sources_news.json')
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                articles = data.get('items', [])
                # Pulisce HTML da tutte le notizie esistenti
                for article in articles:
                    if 'summary' in article:
                        article['summary'] = clean_html(article['summary'])
                    if 'title' in article:
                        article['title'] = clean_html(article['title'])
                return articles
        except Exception as e:
            print(f"Errore caricamento all_sources_news.json: {e}")
            pass
    
    # Fallback: notizie embedded (le 12 migliori)
    return [
        {
            "id": 1,
            "title": "Can OpenAI keep pace with industry's soaring costs?",
            "slug": "can-openai-keep-pace-with-industrys-soaring-costs",
            "url": "https://www.theguardian.com/technology/2025/nov/10/sam-altman-can-openai-profits-keep-pace",
            "summary": "As investor jitters grow, the loss-making ChatGPT firm's vast spending commitments test the limits of Silicon Valley optimism. It is the $1.4tn (£1.1tn) question. How can a loss-making startup such as OpenAI afford such a staggering spending commitment?",
            "author": "Dan Milmo",
            "published_at": "2025-11-11T00:00:00",
            "collected_at": "2025-11-11T00:00:00",
            "source_id": 1,
            "is_featured": True,
            "is_verified": True,
            "is_archived": False,
            "quality_score": 0.75,
            "reading_time_minutes": 3,
            "keywords": ["OpenAI", "costs", "AI", "business"],
            "language": "en"
        },
        {
            "id": 2,
            "title": "What we lose when we surrender care to algorithms | Eric Reinhart",
            "slug": "what-we-lose-when-we-surrender-care-to-algorithms",
            "url": "https://www.theguardian.com/us-news/ng-interactive/2025/nov/09/healthcare-artificial-intelligence-ai",
            "summary": "A dangerous faith in AI is sweeping American healthcare – with consequences for the basis of society itself. The computer interrupted while Pamela was still speaking. I had accompanied her to a recent doctor's appointment.",
            "author": "Eric Reinhart",
            "published_at": "2025-11-11T00:00:00",
            "collected_at": "2025-11-11T00:00:00",
            "source_id": 1,
            "is_featured": False,
            "is_verified": True,
            "is_archived": False,
            "quality_score": 0.8,
            "reading_time_minutes": 4,
            "keywords": ["healthcare", "AI", "algorithms", "society"],
            "language": "en"
        },
        {
            "id": 3,
            "title": "Social media misinformation driving men to seek unneeded NHS testosterone therapy",
            "slug": "social-media-misinformation-testosterone-therapy",
            "url": "https://www.theguardian.com/society/2025/nov/08/social-media-misinformation-driving-men-to-nhs-clinics",
            "summary": "Endocrinologists warn taking testosterone unnecessarily can suppress natural hormone production. Social media misinformation is driving men to NHS clinics in search of testosterone therapy they don't need.",
            "author": "Sarah Marsh",
            "published_at": "2025-11-11T00:00:00",
            "collected_at": "2025-11-11T00:00:00",
            "source_id": 1,
            "is_featured": False,
            "is_verified": True,
            "is_archived": False,
            "quality_score": 0.85,
            "reading_time_minutes": 5,
            "keywords": ["health", "misinformation", "testosterone", "NHS"],
            "language": "en"
        },
        {
            "id": 4,
            "title": "10mila Labubu contraffatti sequestrati a Palermo dalla Guardia di finanza",
            "slug": "labubu-contraffatti-sequestrati-palermo",
            "url": "https://www.wired.it/article/10mila-labubu-contraffatti-sequestrati-a-palermo-dalla-guardia-di-finanza/",
            "summary": "Da Labubu a lafufu, i peluche falsi erano venduti in sette negozi, uno dei quali in un centro commerciale. I commercianti denunciati rischiano accuse per vendita di prodotti con marchi contraffatti.",
            "author": "Riccardo Piccolo",
            "published_at": "2025-11-11T00:00:00",
            "collected_at": "2025-11-11T00:00:00",
            "source_id": 1,
            "is_featured": True,
            "is_verified": True,
            "is_archived": False,
            "quality_score": 0.75,
            "reading_time_minutes": 3,
            "keywords": ["Italia", "contraffazione", "Palermo"],
            "language": "it"
        },
        {
            "id": 5,
            "title": "Audi Q3 e-hybrid, 119 chilometri in solo elettrico con ricarica rapida",
            "slug": "audi-q3-e-hybrid-autonomia-elettrica",
            "url": "https://www.wired.it/article/nuova-audi-q3-e-hybrid-test-su-strada/",
            "summary": "Con un'autonomia elettrica record fino a 119 km, una ricarica rapida in corrente continua da 50 kW e una potenza complessiva di 272 Cv, definisce nuovi standard nel segmento dei Suv compatti premium.",
            "author": "Gabriele Nava",
            "published_at": "2025-11-11T00:00:00",
            "collected_at": "2025-11-11T00:00:00",
            "source_id": 1,
            "is_featured": False,
            "is_verified": True,
            "is_archived": False,
            "quality_score": 0.8,
            "reading_time_minutes": 4,
            "keywords": ["auto", "elettrico", "Audi", "tecnologia"],
            "language": "it"
        },
        {
            "id": 6,
            "title": "Apple rimuove app LGBTQ+ in Cina su richiesta del governo",
            "slug": "apple-rimuove-app-lgbtq-cina",
            "url": "https://www.wired.it/article/blued-finka-app-dating-lgbt-apple-rimozione-app-store-cina/",
            "summary": "Blued e Finka erano tra le piattaforme LGBTQ+ più popolari nel paese, dove la comunità è sempre di più nel mirino del regime di Pechino.",
            "author": "Zeyi Yang, Louise Matsakis",
            "published_at": "2025-11-11T00:00:00",
            "collected_at": "2025-11-11T00:00:00",
            "source_id": 1,
            "is_featured": False,
            "is_verified": True,
            "is_archived": False,
            "quality_score": 0.85,
            "reading_time_minutes": 5,
            "keywords": ["Apple", "Cina", "LGBTQ", "censura"],
            "language": "it"
        },
        {
            "id": 7,
            "title": "Hackers Exploiting Triofox Flaw to Install Remote Access Tools",
            "slug": "hackers-exploiting-triofox-flaw",
            "url": "https://thehackernews.com/2025/11/hackers-exploiting-triofox-flaw-to.html",
            "summary": "Google's Mandiant Threat Defense discovered n-day exploitation of a now-patched security flaw in Gladinet's Triofox file-sharing platform. The critical vulnerability (CVE-2025-12480, CVSS 9.1) allows attackers to bypass authentication.",
            "author": "The Hacker News",
            "published_at": "2025-11-11T00:00:00",
            "collected_at": "2025-11-11T00:00:00",
            "source_id": 1,
            "is_featured": True,
            "is_verified": True,
            "is_archived": False,
            "quality_score": 0.75,
            "reading_time_minutes": 3,
            "keywords": ["cybersecurity", "exploit", "Triofox", "hacking"],
            "language": "en"
        },
        {
            "id": 8,
            "title": "Konni Hackers Turn Google's Find Hub into Remote Data-Wiping Weapon",
            "slug": "konni-hackers-google-find-hub",
            "url": "https://thehackernews.com/2025/11/konni-hackers-turn-googles-find-hub.html",
            "summary": "The North Korea-affiliated threat actor Konni has been attributed to new attacks targeting Android and Windows devices for data theft and remote control. Attackers impersonated psychological counselors and North Korean human rights activists.",
            "author": "The Hacker News",
            "published_at": "2025-11-11T00:00:00",
            "collected_at": "2025-11-11T00:00:00",
            "source_id": 1,
            "is_featured": False,
            "is_verified": True,
            "is_archived": False,
            "quality_score": 0.8,
            "reading_time_minutes": 4,
            "keywords": ["North Korea", "hacking", "Google", "cybersecurity"],
            "language": "en"
        },
        {
            "id": 9,
            "title": "Weekly Recap: Hyper-V Malware, Malicious AI Bots, RDP Exploits",
            "slug": "weekly-recap-hyper-v-malware-ai-bots",
            "url": "https://thehackernews.com/2025/11/weekly-recap-hyper-v-malware-malicious.html",
            "summary": "Cyber threats didn't slow down last week—and attackers are getting smarter. We're seeing malware hidden in virtual machines, side-channel leaks exposing AI chats, and spyware quietly targeting Android devices in the wild.",
            "author": "The Hacker News",
            "published_at": "2025-11-11T00:00:00",
            "collected_at": "2025-11-11T00:00:00",
            "source_id": 1,
            "is_featured": False,
            "is_verified": True,
            "is_archived": False,
            "quality_score": 0.85,
            "reading_time_minutes": 5,
            "keywords": ["malware", "AI", "security", "recap"],
            "language": "en"
        },
        {
            "id": 10,
            "title": "Fire TV Stick: blocco delle app pirata anche in Italia",
            "slug": "fire-tv-stick-blocco-app-pirata-italia",
            "url": "https://www.punto-informatico.it/fire-tv-stick-blocco-app-pirata-italia/",
            "summary": "Amazon inizia a mostrare gli avvisi agli utenti delle app pirata su Fire TV Stick anche in Italia, poi darà il via ai blocchi definitivi.",
            "author": "Cristiano Ghidotti",
            "published_at": "2025-11-11T00:00:00",
            "collected_at": "2025-11-11T00:00:00",
            "source_id": 1,
            "is_featured": True,
            "is_verified": True,
            "is_archived": False,
            "quality_score": 0.75,
            "reading_time_minutes": 3,
            "keywords": ["Amazon", "Fire TV", "pirateria", "Italia"],
            "language": "it"
        },
        {
            "id": 11,
            "title": "ExpressVPN in offerta: streaming, viaggi e privacy totale",
            "slug": "expressvpn-offerta-streaming-privacy",
            "url": "https://www.punto-informatico.it/streaming-viaggi-e-privacy-totale-expressvpn-in-offerta/",
            "summary": "Naviga in modo sicuro e veloce con ExpressVPN: ora il piano biennale è scontato del 67% e include 4 mesi extra gratis per una protezione completa.",
            "author": "Eleonora Busi",
            "published_at": "2025-11-11T00:00:00",
            "collected_at": "2025-11-11T00:00:00",
            "source_id": 1,
            "is_featured": False,
            "is_verified": True,
            "is_archived": False,
            "quality_score": 0.7,
            "reading_time_minutes": 4,
            "keywords": ["VPN", "privacy", "sicurezza", "offerta"],
            "language": "it"
        },
        {
            "id": 12,
            "title": "Hostinger Black Friday: sito online a meno di 2€ al mese",
            "slug": "hostinger-black-friday-hosting-economico",
            "url": "https://www.punto-informatico.it/hostinger-sconti-black-friday/",
            "summary": "Hosting super scontato per il Black Friday: sconti fino all'85% sui piani Hostinger, con dominio incluso e 3 mesi gratis. Ideale per siti web, blog e e-commerce.",
            "author": "Eleonora Busi",
            "published_at": "2025-11-11T00:00:00",
            "collected_at": "2025-11-11T00:00:00",
            "source_id": 1,
            "is_featured": False,
            "is_verified": True,
            "is_archived": False,
            "quality_score": 0.7,
            "reading_time_minutes": 5,
            "keywords": ["hosting", "Hostinger", "Black Friday", "sconti"],
            "language": "it"
        }
    ]


@app.get("/api/v1/articles")
def get_articles(category_id: int = None, skip: int = 0, limit: int = 20):
    """Get articles - REAL NEWS from RSS feeds - WITH CATEGORY FILTER AND PAGINATION"""
    articles = _load_articles()
    
    # Mappa categorie → keywords da cercare
    CATEGORY_KEYWORDS = {
        1: ["technology", "tech", "tecnologia", "computer", "software", "hardware", "digital"],  # Technology
        2: ["science", "scienz", "research", "ricerca", "studio", "arxiv"],  # Science
        3: ["philosophy", "filosofia", "pensiero", "critica"],  # Philosophy
        4: ["cybersecurity", "security", "sicurezza", "hacking", "exploit", "malware", "cyber"],  # Cybersecurity
        5: ["ai", "artificial intelligence", "intelligenza artificiale", "machine learning", "gpt", "openai", "llm"],  # AI
        6: ["innovation", "innovazione", "futuro", "new"],  # Innovation
        7: ["culture", "cultura", "arte", "society", "società"],  # Culture
        8: ["ethics", "etica", "morale", "diritti"],  # Ethics
        9: ["sport", "calcio", "football", "soccer", "tennis", "basketball", "sports"],  # Sport
        10: ["nature", "ambiente", "environment", "climate", "clima", "green", "ecologia"],  # Nature
        11: ["business", "economia", "finance", "finanza", "market", "mercato", "company", "azienda"],  # Business
        12: ["health", "salute", "medical", "medico", "hospital", "ospedale", "medicine"],  # Health
        13: ["politics", "politica", "government", "governo", "election", "elezioni", "parliament"],  # Politics
        14: ["entertainment", "intrattenimento", "movie", "film", "cinema", "music", "musica", "tv", "show"]  # Entertainment
    }
    
    if articles:
        # Filtra per categoria se richiesto
        if category_id and category_id in CATEGORY_KEYWORDS:
            cat_keywords = CATEGORY_KEYWORDS[category_id]
            filtered = []
            
            for article in articles:
                # Cerca match nei keywords dell'articolo
                article_keywords = [k.lower() for k in article.get('keywords', [])]
                article_title = article.get('title', '').lower()
                article_summary = article.get('summary', '').lower()
                
                # Match se almeno una keyword della categoria è presente
                for cat_kw in cat_keywords:
                    if any(cat_kw in akw for akw in article_keywords) or \
                       cat_kw in article_title or \
                       cat_kw in article_summary:
                        filtered.append(article)
                        break
            
            articles = filtered
        
        # Applica paginazione
        total = len(articles)
        paginated_articles = articles[skip:skip + limit]
        
        return {
            "items": paginated_articles,
            "total": total,
            "page": (skip // limit) + 1,
            "size": len(paginated_articles),
            "pages": (total + limit - 1) // limit if limit > 0 else 1
        }
    
    # Fallback to demo if file not found
    return {
        "items": [],
        "total": 0,
        "page": 1,
        "size": 0,
        "pages": 1
        }


@app.get("/api/v1/categories")
def get_categories():
    """Get categories - demo data"""
    return [
        {"id": 1, "name": "Technology", "slug": "technology", "icon": "computer", "color": "#2196F3"},
        {"id": 2, "name": "Science", "slug": "science", "icon": "science", "color": "#4CAF50"},
        {"id": 3, "name": "Philosophy", "slug": "philosophy", "icon": "psychology", "color": "#9C27B0"},
        {"id": 4, "name": "Cybersecurity", "slug": "cybersecurity", "icon": "security", "color": "#F44336"},
        {"id": 5, "name": "AI", "slug": "ai", "icon": "smart_toy", "color": "#FF9800"},
        {"id": 6, "name": "Innovation", "slug": "innovation", "icon": "lightbulb", "color": "#FFEB3B"},
        {"id": 7, "name": "Culture", "slug": "culture", "icon": "palette", "color": "#E91E63"},
        {"id": 8, "name": "Ethics", "slug": "ethics", "icon": "balance", "color": "#607D8B"},
        {"id": 9, "name": "Sport", "slug": "sport", "icon": "sports_soccer", "color": "#FF5722"},
        {"id": 10, "name": "Nature", "slug": "nature", "icon": "park", "color": "#4CAF50"},
        {"id": 11, "name": "Business", "slug": "business", "icon": "business_center", "color": "#1976D2"},
        {"id": 12, "name": "Health", "slug": "health", "icon": "health_and_safety", "color": "#E91E63"},
        {"id": 13, "name": "Politics", "slug": "politics", "icon": "gavel", "color": "#9C27B0"},
        {"id": 14, "name": "Entertainment", "slug": "entertainment", "icon": "movie", "color": "#FF9800"}
    ]


@app.get("/api/v1/articles/{article_id}")
def get_article(article_id: int):
    """Get single article by ID"""
    articles = _load_articles()
    
    for article in articles:
        if article.get('id') == article_id:
            return article
    
    return {"error": "Article not found"}


@app.get("/api/v1/articles/slug/{slug}")
def get_article_by_slug(slug: str):
    """Get single article by slug"""
    articles = _load_articles()
    
    for article in articles:
        if article.get('slug') == slug:
            return article
    
    return {"error": "Article not found"}


@app.get("/api/v1/articles/featured/list")
def get_featured_articles(limit: int = 10):
    """Get featured articles"""
    articles = _load_articles()
    
    # Filtra solo gli articoli in evidenza
    featured = [a for a in articles if a.get('is_featured', False)]
    
    # Ordina per quality score (decrescente)
    featured.sort(key=lambda x: x.get('quality_score', 0), reverse=True)
    
    # Limita il numero
    return featured[:limit]


@app.get("/api/v1/articles/recent/list")
def get_recent_articles(days: int = 7, limit: int = 20):
    """Get recent articles"""
    articles = _load_articles()
    
    # Ordina per data pubblicazione (più recenti prima)
    articles.sort(key=lambda x: x.get('published_at', ''), reverse=True)
    
    # Limita il numero
    return articles[:limit]


@app.post("/api/v1/articles/search")
def search_articles(query: str = "", category_id: int = None, language: str = ""):
    """Search articles by query - FULL TEXT SEARCH"""
    articles = _load_articles()
    
    if not articles:
        return {
            "items": [],
            "total": 0,
            "page": 1,
            "size": 0,
            "pages": 1
        }
    
    results = []
    query_lower = query.lower() if query else ""
    
    for article in articles:
        # Se c'è una query, cerca nel titolo, sommario e keywords
        if query_lower:
            title = article.get('title', '').lower()
            summary = article.get('summary', '').lower()
            keywords = ' '.join(article.get('keywords', [])).lower()
            
            # Match se la query è nel titolo, sommario o keywords
            if query_lower not in title and \
               query_lower not in summary and \
               query_lower not in keywords:
                continue
        
        # Filtra per categoria se richiesto
        if category_id:
            # Usa la stessa logica del filtro categorie
            CATEGORY_KEYWORDS = {
                1: ["technology", "tech", "tecnologia", "ai", "computer", "software", "hardware", "digital"],
                2: ["science", "scienz", "research", "ricerca", "studio"],
                3: ["philosophy", "filosofia", "pensiero", "critica"],
                4: ["cybersecurity", "security", "sicurezza", "hacking", "exploit", "malware", "cyber"],
                5: ["ai", "artificial intelligence", "intelligenza artificiale", "machine learning", "gpt", "openai", "llm"],
                6: ["innovation", "innovazione", "futuro", "new"],
                7: ["culture", "cultura", "arte", "society", "società"],
                8: ["ethics", "etica", "morale", "diritti"]
            }
            
            if category_id in CATEGORY_KEYWORDS:
                cat_keywords = CATEGORY_KEYWORDS[category_id]
                article_keywords = [k.lower() for k in article.get('keywords', [])]
                article_title = article.get('title', '').lower()
                article_summary = article.get('summary', '').lower()
                
                match = False
                for cat_kw in cat_keywords:
                    if any(cat_kw in akw for akw in article_keywords) or \
                       cat_kw in article_title or \
                       cat_kw in article_summary:
                        match = True
                        break
                
                if not match:
                    continue
        
        # Filtra per lingua se richiesto
        if language and article.get('language', '') != language:
            continue
        
        results.append(article)
    
    return {
        "items": results,
        "total": len(results),
        "page": 1,
        "size": len(results),
        "pages": 1
    }


@app.get("/api/v1/sources")
def get_sources():
    """Get sources - demo data"""
    return [
        {
            "id": 1,
            "name": "SINTESI News",
            "slug": "sintesi",
            "url": "https://newsflow-orcin.vercel.app",
            "source_type": "rss",
            "language": "it",
            "is_active": True,
            "is_verified": True
        }
    ]


@app.get("/api/v1/auth/whoami")
def whoami(request: Request):
    """
    Autenticazione automatica con fingerprint
    Zero friction - 100% conversion!
    
    Returns user data (esistente o nuovo)
    """
    # Genera fingerprint da request
    request_data = {
        'ip': request.client.host if request.client else 'unknown',
        'user_agent': request.headers.get('user-agent', 'unknown'),
        'accept_language': request.headers.get('accept-language', 'unknown'),
        'accept_encoding': request.headers.get('accept-encoding', 'unknown')
    }
    
    fingerprint = FingerprintAuth.generate_fingerprint(request_data)
    
    # Carica o crea file users (localStorage-like server-side)
    users_file = 'users_db.json'
    
    try:
        with open(users_file, 'r', encoding='utf-8') as f:
            users = json.load(f)
    except:
        users = {}
    
    # Cerca utente per fingerprint
    if fingerprint in users:
        # Utente esistente!
        user = users[fingerprint]
        user['is_new'] = False
        
        # Aggiorna last_seen
        from datetime import datetime
        user['last_seen'] = datetime.utcnow().isoformat()
        
        # Salva
        with open(users_file, 'w', encoding='utf-8') as f:
            json.dump(users, f, indent=2, ensure_ascii=False)
        
        return {
            "success": True,
            "authenticated": True,
            "user": user
        }
    
    # Nuovo utente - crea!
    user_data = FingerprintAuth.create_user_data(fingerprint)
    user_data['id'] = len(users) + 1
    user_data['is_new'] = True
    
    # Salva
    users[fingerprint] = user_data
    
    with open(users_file, 'w', encoding='utf-8') as f:
        json.dump(users, f, indent=2, ensure_ascii=False)
    
    return {
        "success": True,
        "authenticated": True,
        "user": user_data,
        "message": f"Benvenuto {user_data['name']}! 🎉"
    }


@app.post("/api/admin/collect-news")
def trigger_news_collection():
    """
    Endpoint per raccogliere nuovi articoli AUTOMATICAMENTE.
    Può essere chiamato da un CRON job gratuito ogni 4 ore.
    
    Usa cron-job.org (gratuito) per chiamare questo endpoint:
    URL: https://newsflow-backend-v2.onrender.com/api/admin/collect-news
    Frequenza: Ogni 4 ore
    """
    import feedparser
    import json
    import os
    import re
    from datetime import datetime
    
    def clean_html(text):
        """Rimuove tutti i tag HTML dal testo"""
        if not text:
            return ""
        import html
        # Rimuove tutti i tag HTML
        text = re.sub(r'<[^>]+>', '', text)
        # Decodifica entità HTML (inclusi quelli numerici come &#8217;)
        try:
            text = html.unescape(text)
        except:
            # Fallback manuale se html.unescape non disponibile
            text = text.replace('&nbsp;', ' ')
            text = text.replace('&amp;', '&')
            text = text.replace('&lt;', '<')
            text = text.replace('&gt;', '>')
            text = text.replace('&quot;', '"')
            text = text.replace('&#39;', "'")
            text = text.replace('&apos;', "'")
            # Decodifica entità numeriche comuni
            text = text.replace('&#8217;', "'")  # apostrofo
            text = text.replace('&#8216;', "'")  # apostrofo sinistro
            text = text.replace('&#8220;', '"')  # virgolette sinistre
            text = text.replace('&#8221;', '"')  # virgolette destre
            text = text.replace('&#8230;', '...')  # tre puntini
            text = text.replace('&mdash;', '—')  # dash
            text = text.replace('&ndash;', '–')  # en dash
        # Rimuove spazi multipli
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    try:
        print("🔄 Aggiornamento automatico notizie iniziato...")
        
        # Importa traduttore (opzionale, se disponibile)
        try:
            from deep_translator import GoogleTranslator
            translator = GoogleTranslator(source='en', target='it')
            translation_available = True
        except ImportError:
            print("⚠️  deep_translator non disponibile - traduzione disabilitata")
            translation_available = False
            translator = None
        
        # Fonti RSS - ESPANSE per tutte le categorie
        RSS_SOURCES = {
            # Tecnologia
            'MIT Technology Review': 'https://www.technologyreview.com/feed/',
            'The Guardian Tech': 'https://www.theguardian.com/technology/rss',
            'Wired IT': 'https://www.wired.it/feed/rss',
            'The Hacker News': 'https://feeds.feedburner.com/TheHackersNews',
            'Punto Informatico': 'https://www.punto-informatico.it/feed/',
            'Agenda Digitale': 'https://www.agendadigitale.eu/feed/',
            
            # Scienza
            'ArXiv CS': 'http://export.arxiv.org/rss/cs',
            'Science Daily': 'https://www.sciencedaily.com/rss/all.xml',
            
            # Filosofia
            'MicroMega': 'https://www.micromega.net/feed/',
            
            # Cybersecurity
            'ICT Security Magazine': 'https://www.ictsecuritymagazine.com/feed/',
            
            # Business
            'AI4Business': 'https://www.ai4business.it/feed/',
            'The Guardian Business': 'https://www.theguardian.com/business/rss',
            
            # Sport
            'The Guardian Sport': 'https://www.theguardian.com/sport/rss',
            'Gazzetta dello Sport': 'https://www.gazzetta.it/rss/home.xml',
            
            # Salute
            'The Guardian Health': 'https://www.theguardian.com/society/health/rss',
            
            # Politica
            'The Guardian Politics': 'https://www.theguardian.com/politics/rss',
            
            # Intrattenimento
            'The Guardian Entertainment': 'https://www.theguardian.com/uk/entertainment/rss',
            
            # Natura/Ambiente
            'The Guardian Environment': 'https://www.theguardian.com/environment/rss',
        }
        
        all_articles = []
        article_id = 1
        
        # Raccoglie notizie da tutte le fonti
        for source_name, rss_url in RSS_SOURCES.items():
            try:
                feed = feedparser.parse(rss_url)
                count = 0
                for entry in feed.entries[:5]:
                    try:
                        # Estrae contenuto completo: prova content, poi description, poi summary
                        full_content = ""
                        full_content_html = ""  # Mantiene HTML per estrarre immagini
                        if hasattr(entry, 'content') and entry.content:
                            # Alcuni feed hanno content[0].value con HTML completo
                            if isinstance(entry.content, list) and len(entry.content) > 0:
                                full_content_html = entry.content[0].value
                                full_content = full_content_html
                        elif hasattr(entry, 'description'):
                            full_content_html = entry.description
                            full_content = entry.description
                        elif hasattr(entry, 'summary'):
                            full_content_html = entry.summary
                            full_content = entry.summary
                        
                        # Pulisce HTML dal contenuto completo
                        full_content_clean = clean_html(full_content)
                        
                        # Summary: usa i primi 600 caratteri (aumentato da 400)
                        summary = full_content_clean[:600] if len(full_content_clean) > 600 else full_content_clean
                        
                        # Content completo: tutto il testo pulito (max 5000 caratteri per performance)
                        content = full_content_clean[:5000] if len(full_content_clean) > 5000 else full_content_clean
                        
                        # Determina lingua originale
                        original_language = 'it' if source_name in ['MicroMega', 'AI4Business', 'ICT Security Magazine', 
                                                           'Punto Informatico', 'Agenda Digitale', 'Wired IT', 'Gazzetta dello Sport'] else 'en'
                        language = original_language
                        
                        # Traduci in italiano se la notizia è in inglese
                        if language == 'en' and translation_available and translator:
                            try:
                                import time
                                # Traduci titolo
                                title_en = entry.get('title', '').strip()[:200]
                                if title_en:
                                    title_it = translator.translate(title_en)
                                    time.sleep(0.2)  # Evita rate limiting
                                else:
                                    title_it = title_en
                                
                                # Traduci summary (primi 500 caratteri per evitare limiti API)
                                if summary:
                                    summary_it = translator.translate(summary[:500])
                                    time.sleep(0.3)
                                else:
                                    summary_it = summary
                                
                                # Traduci anche content completo se disponibile (primi 2000 caratteri)
                                if content and len(content) > len(summary):
                                    try:
                                        content_it = translator.translate(content[:2000])
                                        time.sleep(0.5)  # Più tempo per contenuti lunghi
                                        content = content_it if content_it else content
                                    except:
                                        pass  # Se fallisce, usa content originale
                                
                                # Usa versioni tradotte
                                entry_title = title_it if title_it else entry.get('title', '').strip()[:200]
                                summary = summary_it if summary_it else summary
                                language = 'it'  # Ora è in italiano
                                
                            except Exception as e:
                                print(f"⚠️  Errore traduzione: {e}")
                                # Usa originale se traduzione fallisce
                                entry_title = entry.get('title', '').strip()[:200]
                        else:
                            entry_title = entry.get('title', '').strip()[:200]
                        
                        # Determina categoria basandosi sulla fonte
                        if 'Security' in source_name or 'Hacker' in source_name:
                            category = 'Cybersecurity'
                        elif 'ArXiv' in source_name or 'Science' in source_name:
                            category = 'Science'
                        elif 'MicroMega' in source_name:
                            category = 'Philosophy'
                        elif 'Sport' in source_name or 'Gazzetta' in source_name:
                            category = 'Sport'
                        elif 'Business' in source_name or 'AI4Business' in source_name:
                            category = 'Business'
                        elif 'Health' in source_name:
                            category = 'Health'
                        elif 'Politics' in source_name:
                            category = 'Politics'
                        elif 'Entertainment' in source_name:
                            category = 'Entertainment'
                        elif 'Environment' in source_name:
                            category = 'Nature'
                        elif 'AI' in source_name or 'artificial intelligence' in summary.lower():
                            category = 'AI'
                        else:
                            category = 'Technology'
                        
                        # Calcola reading_time basato sulla lunghezza del contenuto
                        content_length = len(content) if content else len(summary)
                        reading_time = max(1, int(content_length / 200))  # ~200 caratteri per minuto
                        
                        # Estrae immagine da vari campi del feed RSS
                        image_url = None
                        
                        # 1. Prova media_content (Media RSS standard)
                        if hasattr(entry, 'media_content') and entry.media_content:
                            if isinstance(entry.media_content, list) and len(entry.media_content) > 0:
                                media_item = entry.media_content[0]
                                if isinstance(media_item, dict) and 'url' in media_item:
                                    image_url = media_item['url']
                                elif isinstance(media_item, str):
                                    image_url = media_item
                        
                        # 2. Prova media_thumbnail
                        if not image_url and hasattr(entry, 'media_thumbnail') and entry.media_thumbnail:
                            if isinstance(entry.media_thumbnail, list) and len(entry.media_thumbnail) > 0:
                                thumb_item = entry.media_thumbnail[0]
                                if isinstance(thumb_item, dict) and 'url' in thumb_item:
                                    image_url = thumb_item['url']
                                elif isinstance(thumb_item, str):
                                    image_url = thumb_item
                        
                        # 3. Prova enclosures (allegati)
                        if not image_url and hasattr(entry, 'enclosures') and entry.enclosures:
                            for enc in entry.enclosures:
                                if isinstance(enc, dict):
                                    enc_type = enc.get('type', '').lower()
                                    if 'image' in enc_type:
                                        image_url = enc.get('href') or enc.get('url')
                                        break
                        
                        # 4. Estrae immagine da HTML nel contenuto
                        if not image_url and full_content_html:
                            import re
                            img_pattern = r'<img[^>]+src=["\']([^"\']+)["\']'
                            img_matches = re.findall(img_pattern, full_content_html, re.IGNORECASE)
                            if img_matches:
                                # Prende la prima immagine trovata
                                image_url = img_matches[0]
                                # Se è un URL relativo, prova a renderlo assoluto
                                if image_url.startswith('//'):
                                    image_url = 'https:' + image_url
                                elif image_url.startswith('/'):
                                    # Prova a costruire URL assoluto dalla fonte
                                    from urllib.parse import urljoin
                                    if entry.get('link'):
                                        image_url = urljoin(entry.get('link'), image_url)
                        
                        # 5. Valida e pulisce URL immagine
                        if image_url:
                            # Rimuove parametri di tracking comuni
                            image_url = image_url.split('?')[0].split('&')[0]
                            # Verifica che sia un URL valido
                            if not image_url.startswith(('http://', 'https://')):
                                image_url = None
                        
                        article = {
                            "id": article_id,
                            "title": entry_title,
                            "slug": entry_title.lower().replace(' ', '-').replace("'", '').replace(',', '')[:50],
                            "url": entry.get('link', ''),
                            "summary": summary,  # Summary più lungo (600 caratteri)
                            "content": content,  # Contenuto completo (fino a 5000 caratteri)
                            "image_url": image_url,  # Immagine estratta dal feed
                            "author": entry.get('author', source_name) + (" (trad. auto)" if original_language == 'en' and language == 'it' else ""),
                            "published_at": datetime.now().isoformat(),
                            "collected_at": datetime.now().isoformat(),
                            "source_id": 1,
                            "is_featured": count == 0,
                            "is_verified": True,
                            "is_archived": False,
                            "quality_score": 0.7 + (0.05 * (5 - count)),
                            "reading_time_minutes": reading_time,
                            "keywords": [category.lower(), "news", language, source_name.lower()],
                            "language": language,
                            "original_language": original_language if original_language != language else None
                        }
                        
                        all_articles.append(article)
                        article_id += 1
                        count += 1
                    except:
                        continue
            except Exception as e:
                print(f"Errore fonte {source_name}: {e}")
                continue
        
        # Aggiorna final_news_italian.json
        output_data = {
            "items": all_articles,
            "total": len(all_articles),
            "page": 1,
            "size": len(all_articles),
            "pages": 1,
            "updated_at": datetime.now().isoformat()
        }
        
        file_path = 'final_news_italian.json'
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        # Gli articoli verranno ricaricati automaticamente alla prossima chiamata a _load_articles()
        print(f"✅ Aggiornate {len(all_articles)} notizie!")
        
        return {
            "success": True,
            "message": f"Collected and updated {len(all_articles)} articles successfully!",
            "total_articles": len(all_articles),
            "updated_at": datetime.now().isoformat(),
            "next_collection": "In 4 hours"
        }
    except Exception as e:
        print(f"❌ Errore aggiornamento: {e}")
        return {
            "success": False,
            "error": str(e)
        }


@app.post("/api/admin/create-youtube-video")
def create_youtube_video(max_articles: int = 5):
    """
    Crea un video YouTube automatico dalle notizie.
    
    Args:
        max_articles: Numero massimo di notizie da includere (default: 5)
    
    Returns:
        Informazioni sul video creato
    """
    return _create_youtube_video_internal(max_articles=max_articles)


@app.post("/api/admin/create-youtube-video-long")
def create_youtube_video_long(duration_minutes: int = 60):
    """
    Crea un video YouTube lungo per playlist 24/7.
    
    Args:
        duration_minutes: Durata target in minuti (default: 60 = 1 ora)
                         Consigliato: 60-120 minuti per video
    
    Returns:
        Informazioni sul video creato
    """
    return _create_youtube_video_internal(target_duration_minutes=duration_minutes)


@app.post("/api/admin/create-youtube-short-video")
def create_youtube_short_video():
    """
    Crea video corto da 2 minuti con solo notizie che hanno immagini.
    Perfetto per live brevi ogni 20 minuti.
    
    Returns:
        Informazioni sul video creato
    """
    try:
        import sys
        import os
        
        # Aggiungi il percorso del backend al PYTHONPATH
        backend_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if backend_path not in sys.path:
            sys.path.insert(0, backend_path)
        
        from youtube_short_video_generator import create_short_video_2min
        
        # Carica articoli
        articles = _load_articles()
        
        if not articles:
            return {
                "success": False,
                "error": "Nessun articolo disponibile"
            }
        
        # Crea video corto (solo notizie con immagini)
        video_path = create_short_video_2min(articles)
        
        if video_path:
            # Calcola durata reale
            try:
                from moviepy.editor import VideoFileClip
                video_clip = VideoFileClip(video_path)
                actual_duration_minutes = round(video_clip.duration / 60, 1)
                video_clip.close()
            except:
                actual_duration_minutes = 2.0
            
            file_size_mb = round(os.path.getsize(video_path) / (1024 * 1024), 2)
            
            return {
                "success": True,
                "video_path": video_path,
                "duration_minutes": actual_duration_minutes,
                "target_duration_minutes": 2,
                "file_size_mb": file_size_mb,
                "articles_count": len(articles),
                "message": "Video corto da 2 minuti creato con successo!"
            }
        else:
            return {
                "success": False,
                "error": "Errore durante la creazione del video"
            }
            
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {
            "success": False,
            "error": str(e)
        }


@app.post("/api/admin/create-youtube-live-video")
def create_youtube_live_video(duration_minutes: int = 30):
    """
    Crea un video per YouTube Live che ripete le notizie fino a raggiungere la durata desiderata.
    Perfetto per trasmettere un telegiornale continuo durante una live.
    
    Args:
        duration_minutes: Durata target del video per la live (default: 30 minuti)
                         Consigliato: 30-60 minuti per live, 240 per TG 4 ore
    
    Returns:
        Informazioni sul video creato
    """
    try:
        import sys
        import os
        # Aggiungi il percorso del backend al PYTHONPATH
        backend_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if backend_path not in sys.path:
            sys.path.insert(0, backend_path)
        
        from youtube_video_generator import YouTubeVideoGenerator
        
        # Carica le notizie
        articles = _load_articles()
        if not articles:
            return {
                "success": False,
                "error": "Nessuna notizia disponibile"
            }
        
        # Crea il generatore video
        generator = YouTubeVideoGenerator(articles)
        
        try:
            # Crea il video per live (ripete le notizie fino alla durata target)
            video_path = generator.create_live_video(duration_minutes=duration_minutes)
            
            if video_path:
                # Calcola durata reale del video
                try:
                    from moviepy.editor import VideoFileClip
                    video_clip = VideoFileClip(video_path)
                    actual_duration_minutes = round(video_clip.duration / 60, 1)
                    video_clip.close()
                except:
                    actual_duration_minutes = duration_minutes
                
                result = {
                    "success": True,
                    "message": f"Video per LIVE creato con successo!",
                    "video_path": video_path,
                    "file_size_mb": round(os.path.getsize(video_path) / (1024 * 1024), 2) if os.path.exists(video_path) else 0,
                    "duration_minutes": actual_duration_minutes,
                    "target_duration_minutes": duration_minutes,
                    "articles_count": len(articles),
                    "repetitions": round(actual_duration_minutes * 60 / (len(articles) * 13), 1)
                }
                
                return result
            else:
                return {
                    "success": False,
                    "error": "Errore nella creazione del video"
                }
        finally:
            try:
                generator.cleanup()
            except:
                pass
                
    except ImportError as e:
        return {
            "success": False,
            "error": f"Dipendenze mancanti: {str(e)}",
            "hint": "Installa con: pip install moviepy gtts pillow"
        }
    except Exception as e:
        import traceback
        return {
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }


@app.post("/api/admin/upload-tg-to-youtube")
def upload_tg_to_youtube():
    """
    Carica automaticamente il video TG su YouTube.
    Richiede YouTube API credentials configurate.
    
    Returns:
        Informazioni sull'upload
    """
    try:
        import sys
        import os
        backend_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if backend_path not in sys.path:
            sys.path.insert(0, backend_path)
        
        from youtube_api_manager import YouTubeAPIManager
        
        # Verifica che il video esista
        video_path = os.path.join(backend_path, "youtube_videos", "newsflow_tg.mp4")
        if not os.path.exists(video_path):
            return {
                "success": False,
                "error": "Video TG non trovato. Crea prima il video con /api/admin/create-tg-video"
            }
        
        # Crea manager YouTube
        manager = YouTubeAPIManager()
        
        # Autentica
        if not manager.authenticate():
            return {
                "success": False,
                "error": "Autenticazione YouTube fallita. Configura le credenziali.",
                "hint": "Vedi: CONFIGURA_YOUTUBE_API.ps1"
            }
        
        # Upload video
        title = f"TG NewsFlow - Notizie del {datetime.now().strftime('%d/%m/%Y')}"
        description = "Telegiornale automatico con le ultime notizie. Aggiornato automaticamente."
        tags = ["notizie", "telegiornale", "news", "italia", "informazione"]
        
        video_id = manager.upload_video(
            video_path=video_path,
            title=title,
            description=description,
            tags=tags,
            privacy_status="public"
        )
        
        if video_id:
            return {
                "success": True,
                "message": "Video caricato su YouTube con successo!",
                "video_id": video_id,
                "video_url": f"https://www.youtube.com/watch?v={video_id}",
                "title": title
            }
        else:
            return {
                "success": False,
                "error": "Errore durante l'upload del video"
            }
            
    except Exception as e:
        import traceback
        return {
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }


@app.post("/api/admin/create-youtube-live-auto")
def create_youtube_live_auto(hour: int, minute: int = 0):
    """
    Crea una live YouTube programmata automaticamente.
    Richiede YouTube API credentials configurate.
    
    Args:
        hour: Ora (0-23)
        minute: Minuto (0-59)
    
    Returns:
        Informazioni sulla live creata
    """
    try:
        import sys
        import os
        from datetime import datetime, timedelta
        backend_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if backend_path not in sys.path:
            sys.path.insert(0, backend_path)
        
        from youtube_api_manager import YouTubeAPIManager
        
        # Calcola data/ora programmata
        now = datetime.now()
        scheduled_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        
        # Se l'ora è già passata oggi, programma per domani
        if scheduled_time < now:
            scheduled_time += timedelta(days=1)
        
        # Crea manager YouTube
        manager = YouTubeAPIManager()
        
        # Autentica
        if not manager.authenticate():
            return {
                "success": False,
                "error": "Autenticazione YouTube fallita. Configura le credenziali.",
                "hint": "Vedi: CONFIGURA_YOUTUBE_API.ps1"
            }
        
        # Crea live broadcast
        title = f"TG NewsFlow Live - {scheduled_time.strftime('%d/%m/%Y %H:%M')}"
        description = "Telegiornale in diretta con le ultime notizie."
        
        broadcast = manager.create_live_broadcast(
            title=title,
            description=description,
            scheduled_start_time=scheduled_time,
            privacy_status="public"
        )
        
        if broadcast:
            return {
                "success": True,
                "message": "Live YouTube creata con successo!",
                "broadcast_id": broadcast['broadcast_id'],
                "title": title,
                "scheduled_start_time": scheduled_time.isoformat(),
                "note": "La live partirà automaticamente all'orario programmato"
            }
        else:
            return {
                "success": False,
                "error": "Errore durante la creazione della live"
            }
            
    except Exception as e:
        import traceback
        return {
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }


@app.post("/api/admin/create-tg-video")
def create_tg_video():
    """
    Crea un video TG con tutte le notizie disponibili (~18-20 minuti).
    Perfetto per live brevi che si accendono e spengono automaticamente.
    
    Returns:
        Informazioni sul video creato
    """
    try:
        import sys
        import os
        backend_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if backend_path not in sys.path:
            sys.path.insert(0, backend_path)
        
        from youtube_video_generator import YouTubeVideoGenerator
        
        # Carica le notizie
        articles = _load_articles()
        if not articles:
            return {
                "success": False,
                "error": "Nessuna notizia disponibile"
            }
        
        # Crea il generatore video
        generator = YouTubeVideoGenerator(articles)
        
        try:
            # Crea video TG con TUTTE le notizie (non ripete, solo le 85 notizie)
            # Durata stimata: ~18-20 minuti
            output_filename = "newsflow_tg.mp4"
            
            # Usa create_video con tutte le notizie (non create_live_video che ripete)
            video_path = generator.create_video(max_articles=999, output_filename=output_filename)
            
            if video_path:
                # Calcola durata reale
                try:
                    from moviepy.editor import VideoFileClip
                    video_clip = VideoFileClip(video_path)
                    actual_duration_minutes = round(video_clip.duration / 60, 1)
                    video_clip.close()
                except:
                    # Stima basata su numero articoli
                    actual_duration_minutes = round(len(articles) * 13 / 60, 1)
                
                result = {
                    "success": True,
                    "message": "Video TG creato con successo!",
                    "video_path": video_path,
                    "file_size_mb": round(os.path.getsize(video_path) / (1024 * 1024), 2) if os.path.exists(video_path) else 0,
                    "duration_minutes": actual_duration_minutes,
                    "articles_count": len(articles),
                    "note": "Video pronto per live di ~20 minuti. Usa AVVIA_SCHEDULER_LIVE.ps1 per programmare live automatiche"
                }
                
                return result
            else:
                return {
                    "success": False,
                    "error": "Errore nella creazione del video"
                }
        finally:
            try:
                generator.cleanup()
            except:
                pass
                
    except Exception as e:
        import traceback
        return {
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }


@app.get("/api/admin/check-tg-sync")
def check_tg_sync():
    """
    Controlla se il video TG deve essere rigenerato (notizie aggiornate)
    
    Returns:
        Stato della sincronizzazione
    """
    try:
        import sys
        import os
        backend_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if backend_path not in sys.path:
            sys.path.insert(0, backend_path)
        
        from news_sync_monitor import NewsSyncMonitor
        
        monitor = NewsSyncMonitor(
            news_file="final_news_italian.json",
            video_file="youtube_videos/newsflow_live_4h.mp4"
        )
        
        should_regenerate = monitor.should_regenerate_video()
        news_update_time = monitor.get_news_update_time()
        
        return {
            "success": True,
            "should_regenerate": should_regenerate,
            "news_update_time": news_update_time.isoformat() if news_update_time else None,
            "video_exists": os.path.exists(monitor.video_file),
            "message": "Video deve essere rigenerato" if should_regenerate else "Video aggiornato"
        }
    except Exception as e:
        import traceback
        return {
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }


def _create_youtube_video_internal(max_articles: int = None, target_duration_minutes: int = None):
    """
    Funzione interna per creare video YouTube
    """
    try:
        import sys
        import os
        # Aggiungi il percorso del backend al PYTHONPATH
        backend_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if backend_path not in sys.path:
            sys.path.insert(0, backend_path)
        
        from youtube_video_generator import YouTubeVideoGenerator
        
        # Carica le notizie
        articles = _load_articles()
        if not articles:
            return {
                "success": False,
                "error": "Nessuna notizia disponibile"
            }
        
        # Crea il generatore video
        generator = YouTubeVideoGenerator(articles)
        
        try:
            # Crea il video
            if target_duration_minutes:
                video_path = generator.create_video(target_duration_minutes=target_duration_minutes)
                # Calcola durata reale del video
                try:
                    from moviepy.editor import VideoFileClip
                    video_clip = VideoFileClip(video_path)
                    actual_duration_minutes = round(video_clip.duration / 60, 1)
                    video_clip.close()
                except:
                    actual_duration_minutes = target_duration_minutes
            else:
                video_path = generator.create_video(max_articles=max_articles or 5)
                actual_duration_minutes = None
            
            if video_path:
                result = {
                    "success": True,
                    "message": f"Video creato con successo!",
                    "video_path": video_path,
                    "file_size_mb": round(os.path.getsize(video_path) / (1024 * 1024), 2) if os.path.exists(video_path) else 0
                }
                
                if target_duration_minutes:
                    result["duration_minutes"] = actual_duration_minutes or target_duration_minutes
                    result["target_duration_minutes"] = target_duration_minutes
                    # Stima articoli inclusi
                    result["articles_count"] = int((actual_duration_minutes or target_duration_minutes) * 4)
                else:
                    result["articles_count"] = min(max_articles or 5, len(articles))
                
                return result
            else:
                return {
                    "success": False,
                    "error": "Errore nella creazione del video"
                }
        finally:
            try:
                generator.cleanup()
            except:
                pass
            
    except ImportError as e:
        return {
            "success": False,
            "error": f"Dipendenze mancanti: {str(e)}",
            "hint": "Installa con: pip install moviepy gtts pillow"
        }
    except Exception as e:
        import traceback
        return {
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }


@app.post("/api/admin/create-daily-schedule")
def create_daily_schedule():
    """Crea programmazione giornaliera standard per YouTube Live"""
    try:
        articles = _load_articles()
        if not articles:
            return {
                "success": False,
                "error": "Nessuna notizia disponibile"
            }
        
        # Programmazione standard: 4 live al giorno
        schedule_config = [
            {"hour": 8, "minute": 0, "duration_minutes": 30, "time_slot": "morning"},
            {"hour": 12, "minute": 0, "duration_minutes": 30, "time_slot": "afternoon"},
            {"hour": 18, "minute": 0, "duration_minutes": 30, "time_slot": "evening"},
            {"hour": 22, "minute": 0, "duration_minutes": 60, "time_slot": "night"},
        ]
        
        # Salva programmazione (puoi salvare su file JSON)
        schedule_file = 'youtube_schedule.json'
        with open(schedule_file, 'w', encoding='utf-8') as f:
            json.dump({
                "created_at": datetime.now().isoformat(),
                "scheduled_streams": schedule_config
            }, f, indent=2, ensure_ascii=False)
        
        return {
            "success": True,
            "message": "Programmazione giornaliera creata!",
            "scheduled_streams": schedule_config,
            "total_streams": len(schedule_config),
            "note": "Avvia AVVIA_SCHEDULER_LIVE.ps1 per eseguire i live automatici"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


@app.post("/api/admin/schedule-youtube-live")
def schedule_youtube_live(hour: int, minute: int = 0, duration_minutes: int = 30):
    """
    Programma un singolo live stream
    
    Args:
        hour: Ora (0-23)
        minute: Minuto (0-59)
        duration_minutes: Durata del live
    """
    try:
        if not (0 <= hour <= 23):
            return {"success": False, "error": "Ora deve essere tra 0 e 23"}
        if not (0 <= minute <= 59):
            return {"success": False, "error": "Minuto deve essere tra 0 e 59"}
        
        # Carica programmazione esistente
        schedule_file = 'youtube_schedule.json'
        if os.path.exists(schedule_file):
            with open(schedule_file, 'r', encoding='utf-8') as f:
                schedule_data = json.load(f)
        else:
            schedule_data = {"scheduled_streams": []}
        
        # Determina time slot
        time_slot = "morning" if 6 <= hour < 12 else \
                   "afternoon" if 12 <= hour < 18 else \
                   "evening" if 18 <= hour < 22 else "night"
        
        # Aggiungi nuovo stream
        new_stream = {
            "hour": hour,
            "minute": minute,
            "duration_minutes": duration_minutes,
            "time_slot": time_slot
        }
        
        schedule_data["scheduled_streams"].append(new_stream)
        schedule_data["updated_at"] = datetime.now().isoformat()
        
        # Salva
        with open(schedule_file, 'w', encoding='utf-8') as f:
            json.dump(schedule_data, f, indent=2, ensure_ascii=False)
        
        return {
            "success": True,
            "message": f"Live programmato alle {hour:02d}:{minute:02d}",
            "scheduled_stream": new_stream
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


@app.get("/api/admin/youtube-schedule")
def get_youtube_schedule():
    """Ottieni la programmazione YouTube attuale"""
    try:
        schedule_file = 'youtube_schedule.json'
        if os.path.exists(schedule_file):
            with open(schedule_file, 'r', encoding='utf-8') as f:
                schedule_data = json.load(f)
            return {
                "success": True,
                "scheduled_streams": schedule_data.get("scheduled_streams", []),
                "created_at": schedule_data.get("created_at"),
                "updated_at": schedule_data.get("updated_at")
            }
        else:
            return {
                "success": True,
                "scheduled_streams": [],
                "message": "Nessuna programmazione trovata. Usa /api/admin/create-daily-schedule per crearne una."
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main_simple:app", host="0.0.0.0", port=8000, reload=True)

