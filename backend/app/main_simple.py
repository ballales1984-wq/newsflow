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


@app.get("/api/v1/articles")
def get_articles():
    """Get articles - demo data"""
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

