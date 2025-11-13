# Integrazione Google News

## 📰 Descrizione

Google News è stato integrato come fonte di approvvigionamento delle notizie per NewsFlow. Il sistema ora raccoglie automaticamente notizie da Google News utilizzando i feed RSS ufficiali.

## 🔧 Implementazione

### Nuovo Collector

È stato creato un nuovo collector dedicato: `app/services/collectors/google_news_collector.py`

**Caratteristiche:**
- Supporta raccolta da topic/categorie (TECHNOLOGY, SCIENCE, WORLD, BUSINESS, HEALTH, SPORTS, ecc.)
- Supporta ricerca per query specifiche
- Configurabile per lingua e paese (default: italiano, Italia)
- Gestisce parsing automatico degli articoli

### Integrazione nel Sistema

Il collector è stato integrato nell'endpoint `/api/admin/collect-news` in `app/main_simple.py`:

1. **Raccolta da Topic Principali:**
   - TECHNOLOGY
   - SCIENCE
   - WORLD
   - BUSINESS
   - HEALTH
   - SPORTS

2. **Raccolta da Query Specifiche:**
   - intelligenza artificiale
   - cybersecurity
   - innovazione
   - startup

## 📊 Configurazione

### Topic Disponibili

```python
GOOGLE_NEWS_TOPICS = {
    'TECHNOLOGY': 'TECHNOLOGY',
    'SCIENCE': 'SCIENCE',
    'WORLD': 'WORLD',
    'NATION': 'NATION',
    'BUSINESS': 'BUSINESS',
    'ENTERTAINMENT': 'ENTERTAINMENT',
    'SPORTS': 'SPORTS',
    'HEALTH': 'HEALTH',
    'POLITICS': 'POLITICS',
    'ENVIRONMENT': 'ENVIRONMENT',
}
```

### Query Predefinite (Italiano)

```python
GOOGLE_NEWS_QUERIES_IT = [
    'tecnologia',
    'scienza',
    'intelligenza artificiale',
    'cybersecurity',
    'innovazione',
    'startup',
    'economia',
    'politica',
    'sport',
    'salute',
    'ambiente',
    'cultura',
]
```

## 🚀 Utilizzo

### Raccolta Automatica

La raccolta da Google News avviene automaticamente quando viene chiamato l'endpoint:

```
POST /api/admin/collect-news
```

Questo endpoint viene chiamato automaticamente dallo script `AGGIORNA_NOTIZIE.ps1`.

### Utilizzo Programmatico

```python
from app.services.collectors.google_news_collector import GoogleNewsCollector

# Crea collector
collector = GoogleNewsCollector()

# Raccogli da un topic
articles = collector.collect(
    query=None,
    language='it',
    country='IT',
    max_articles=10,
    topic='TECHNOLOGY'
)

# Raccogli da una query
articles = collector.collect(
    query='intelligenza artificiale',
    language='it',
    country='IT',
    max_articles=10
)

# Raccogli da più topic
from app.services.collectors.google_news_collector import GOOGLE_NEWS_TOPICS

articles = collector.collect_by_topics(
    topics=['TECHNOLOGY', 'SCIENCE'],
    language='it',
    country='IT',
    max_articles_per_topic=5
)
```

## 📝 Note Tecniche

- **Feed RSS:** Google News utilizza feed RSS pubblici, quindi non sono necessarie API key
- **Rate Limiting:** Google News può limitare le richieste se troppo frequenti
- **Lingua:** Default italiano (it) per Italia (IT)
- **Categorizzazione:** Gli articoli vengono automaticamente categorizzati in base al topic/query

## ✅ Stato

✅ Collector creato e testato
✅ Integrato nel sistema di raccolta principale
✅ Supporto per topic e query
✅ Categorizzazione automatica
✅ Gestione errori e logging

## 🔄 Prossimi Passi (Opzionali)

- Aggiungere più query personalizzate
- Implementare caching per ridurre richieste duplicate
- Aggiungere supporto per altri paesi/lingue
- Implementare deduplicazione avanzata degli articoli

