"""Initialize database with default data"""
from app.core.database import SessionLocal, engine, Base
from app.models import Category, Source
from slugify import slugify

# Create all tables
Base.metadata.create_all(bind=engine)

def init_categories():
    """Create default categories"""
    db = SessionLocal()
    
    categories = [
        {
            "name": "Technology",
            "description": "Latest in tech, gadgets, and innovation",
            "icon": "computer",
            "color": "#2196F3"
        },
        {
            "name": "Science",
            "description": "Scientific discoveries and research",
            "icon": "science",
            "color": "#4CAF50"
        },
        {
            "name": "Philosophy",
            "description": "Philosophical thought and reflection",
            "icon": "psychology",
            "color": "#9C27B0"
        },
        {
            "name": "Cybersecurity",
            "description": "Security, privacy, and digital protection",
            "icon": "security",
            "color": "#F44336"
        },
        {
            "name": "Artificial Intelligence",
            "description": "AI, machine learning, and automation",
            "icon": "smart_toy",
            "color": "#FF9800"
        },
        {
            "name": "Innovation",
            "description": "Breakthrough ideas and solutions",
            "icon": "lightbulb",
            "color": "#FFEB3B"
        },
        {
            "name": "Culture",
            "description": "Arts, literature, and cultural critique",
            "icon": "palette",
            "color": "#E91E63"
        },
        {
            "name": "Ethics",
            "description": "Ethical debates and moral philosophy",
            "icon": "balance",
            "color": "#607D8B"
        },
        {
            "name": "Sport",
            "description": "Sports news, events, and competitions",
            "icon": "sports_soccer",
            "color": "#FF5722"
        },
        {
            "name": "Nature",
            "description": "Environment, wildlife, and nature conservation",
            "icon": "park",
            "color": "#4CAF50"
        },
        {
            "name": "Business",
            "description": "Economy, finance, and business news",
            "icon": "business_center",
            "color": "#1976D2"
        },
        {
            "name": "Health",
            "description": "Healthcare, wellness, and medical research",
            "icon": "health_and_safety",
            "color": "#E91E63"
        },
        {
            "name": "Politics",
            "description": "Political news and government affairs",
            "icon": "gavel",
            "color": "#9C27B0"
        },
        {
            "name": "Entertainment",
            "description": "Movies, music, TV shows, and celebrities",
            "icon": "movie",
            "color": "#FF9800"
        }
    ]
    
    for cat_data in categories:
        existing = db.query(Category).filter(
            Category.slug == slugify(cat_data["name"])
        ).first()
        
        if not existing:
            category = Category(
                name=cat_data["name"],
                slug=slugify(cat_data["name"]),
                description=cat_data["description"],
                icon=cat_data["icon"],
                color=cat_data["color"]
            )
            db.add(category)
    
    db.commit()
    print(f"Created {len(categories)} categories")
    db.close()


def init_sources():
    """Create default sources"""
    db = SessionLocal()
    
    sources = [
        {
            "name": "MicroMega",
            "url": "https://www.micromega.net",
            "rss_url": "https://www.micromega.net/feed/",
            "source_type": "rss",
            "language": "it",
            "country": "IT",
            "category": "culture"
        },
        {
            "name": "AI4Business",
            "url": "https://www.ai4business.it",
            "rss_url": "https://www.ai4business.it/feed/",
            "source_type": "rss",
            "language": "it",
            "country": "IT",
            "category": "technology"
        },
        {
            "name": "MIT Technology Review",
            "url": "https://www.technologyreview.com",
            "rss_url": "https://www.technologyreview.com/feed/",
            "source_type": "rss",
            "language": "en",
            "country": "US",
            "category": "technology"
        },
        {
            "name": "ICT Security Magazine",
            "url": "https://www.ictsecuritymagazine.com",
            "rss_url": "https://www.ictsecuritymagazine.com/feed/",
            "source_type": "rss",
            "language": "it",
            "country": "IT",
            "category": "cybersecurity"
        },
        {
            "name": "The Guardian Tech",
            "url": "https://www.theguardian.com/technology",
            "rss_url": "https://www.theguardian.com/technology/rss",
            "source_type": "rss",
            "language": "en",
            "country": "UK",
            "category": "technology"
        },
        {
            "name": "Wired Italia",
            "url": "https://www.wired.it",
            "rss_url": "https://www.wired.it/feed/rss",
            "source_type": "rss",
            "language": "it",
            "country": "IT",
            "category": "technology"
        },
        {
            "name": "The Hacker News",
            "url": "https://thehackernews.com",
            "rss_url": "https://feeds.feedburner.com/TheHackersNews",
            "source_type": "rss",
            "language": "en",
            "country": "US",
            "category": "cybersecurity"
        }
    ]
    
    for src_data in sources:
        existing = db.query(Source).filter(
            Source.slug == slugify(src_data["name"])
        ).first()
        
        if not existing:
            source = Source(
                name=src_data["name"],
                slug=slugify(src_data["name"]),
                url=src_data["url"],
                rss_url=src_data["rss_url"],
                source_type=src_data["source_type"],
                language=src_data["language"],
                country=src_data["country"],
                category=src_data["category"],
                is_active=True
            )
            db.add(source)
    
    db.commit()
    print(f"Created {len(sources)} sources")
    db.close()


if __name__ == "__main__":
    print("Initializing database...")
    init_categories()
    init_sources()
    print("Database initialization complete!")

