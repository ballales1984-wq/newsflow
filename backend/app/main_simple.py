"""Versione semplificata di main.py per deploy veloce senza dipendenze complesse"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

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
    
    # Usa il file finale con tutte le notizie in italiano
    file_path = 'final_news_italian.json'
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('items', [])
        except:
            pass
    
    # Fallback su tutte le fonti
    file_path = 'all_sources_news.json'
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('items', [])
        except:
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
def get_articles():
    """Get articles - REAL NEWS from RSS feeds"""
    articles = _load_articles()
    
    if articles:
        return {
            "items": articles,
            "total": len(articles),
            "page": 1,
            "size": 20,
            "pages": 1
        }
    
    # Fallback to demo if file not found
    return {
        "items": [
            {
                "id": 1,
                "title": "NewsFlow è online! 🎉",
                "slug": "newsflow-online",
                "url": "https://newsflow-orcin.vercel.app",
                "summary": "La piattaforma di news curation intelligente è ora disponibile!",
                "author": "Sistema NewsFlow",
                "published_at": "2024-11-11T00:00:00",
                "collected_at": "2024-11-11T00:00:00",
                "source_id": 1,
                "is_featured": True,
                "is_verified": True,
                "is_archived": False,
                "quality_score": 0.95,
                "reading_time_minutes": 2,
                "keywords": ["newsflow", "launch", "ai", "news"],
                "language": "it"
            },
            {
                "id": 2,
                "title": "Super Almanacco Digitale: La Visione",
                "slug": "super-almanacco-visione",
                "url": "https://github.com/ballales1984-wq/newsflow",
                "summary": "Mining di notizie di valore, TG AI, streaming 24/7, edizioni territoriali e molto altro in arrivo!",
                "author": "Redazione SINTESI",
                "published_at": "2024-11-11T00:00:00",
                "collected_at": "2024-11-11T00:00:00",
                "source_id": 1,
                "is_featured": True,
                "is_verified": True,
                "is_archived": False,
                "quality_score": 0.92,
                "reading_time_minutes": 5,
                "keywords": ["almanacco", "ai", "giornalismo", "innovazione"],
                "language": "it"
            },
            {
                "id": 3,
                "title": "Testata SINTESI: Manifesto Fondativo",
                "slug": "sintesi-manifesto",
                "url": "https://newsflow-orcin.vercel.app",
                "summary": "Notizie curate dall'intelligenza critica. Imparzialità algoritmica, confronto sistemico, rispetto del tempo.",
                "author": "Fondatori SINTESI",
                "published_at": "2024-11-11T00:00:00",
                "collected_at": "2024-11-11T00:00:00",
                "source_id": 1,
                "is_featured": False,
                "is_verified": True,
                "is_archived": False,
                "quality_score": 0.89,
                "reading_time_minutes": 3,
                "keywords": ["sintesi", "manifesto", "giornalismo", "etica"],
                "language": "it"
            }
        ],
        "total": 3,
        "page": 1,
        "size": 20,
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
        {"id": 8, "name": "Ethics", "slug": "ethics", "icon": "balance", "color": "#607D8B"}
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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main_simple:app", host="0.0.0.0", port=8000, reload=True)

