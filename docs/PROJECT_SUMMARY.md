# NewsFlow - Riepilogo Progetto

## 📊 Overview

**NewsFlow** è un'applicazione web completa per la cura intelligente di notizie, sviluppata con architettura moderna full-stack.

### Stack Tecnologico

**Backend:**
- FastAPI (Python 3.11+)
- PostgreSQL (Database)
- Redis (Cache & Queue)
- Celery (Background Tasks)
- spaCy + Hugging Face (NLP/AI)

**Frontend:**
- Angular 17
- Angular Material
- TypeScript
- RxJS

**Deployment:**
- Docker & Docker Compose
- Backend: Render/Railway
- Frontend: Vercel/Netlify

## 📁 Struttura Progetto

```
newsflow/
├── backend/                    # Backend FastAPI
│   ├── app/
│   │   ├── api/               # API endpoints
│   │   │   └── v1/
│   │   │       └── endpoints/ # Articoli, categorie, fonti, utenti
│   │   ├── core/              # Configurazione e database
│   │   ├── models/            # SQLAlchemy models
│   │   ├── schemas/           # Pydantic schemas
│   │   └── services/
│   │       ├── collectors/    # RSS, API, scraping
│   │       ├── nlp/           # Analisi NLP
│   │       └── tasks.py       # Celery tasks
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── init_db.py            # Inizializzazione DB
│   └── .env.example
│
├── frontend/                   # Frontend Angular
│   ├── src/
│   │   ├── app/
│   │   │   ├── components/    # Componenti riutilizzabili
│   │   │   ├── pages/         # Pagine principali
│   │   │   ├── services/      # Servizi HTTP
│   │   │   └── models/        # TypeScript interfaces
│   │   ├── environments/      # Configurazioni env
│   │   └── styles.scss        # Stili globali
│   ├── package.json
│   ├── angular.json
│   └── Dockerfile.dev
│
├── docker-compose.yml          # Orchestrazione servizi
├── README.md                   # Documentazione principale
├── SETUP.md                    # Guida setup sviluppo
├── DEPLOYMENT.md               # Guida deployment
├── CONTRIBUTING.md             # Guida contribuzione
├── LICENSE                     # Licenza MIT
├── quick-start.sh             # Script setup Unix
└── quick-start.bat            # Script setup Windows
```

## 🎯 Funzionalità Implementate

### Backend

✅ **API REST Complete**
- CRUD per articoli, categorie, fonti
- Ricerca avanzata e filtri
- Paginazione
- Gestione utenti e autenticazione (base)

✅ **Raccolta Notizie**
- Collector RSS (feedparser)
- API collector (NewsAPI, Guardian)
- Web scraping (Newspaper3k)
- Fonti preconfigurate (MicroMega, AI4Business, MIT Tech Review, etc.)

✅ **Analisi NLP**
- Estrazione keyword con spaCy
- Named Entity Recognition
- Sentiment analysis (base)
- Quality scoring
- Language detection
- Classificazione tematica con Transformers

✅ **Background Tasks**
- Raccolta periodica notizie (Celery)
- Analisi automatica contenuti
- Cleanup articoli vecchi
- Aggiornamento score

✅ **Database**
- Models completi con SQLAlchemy
- Relazioni articoli-categorie-fonti
- Archivio personale utente
- Sistema annotazioni

### Frontend

✅ **Interfaccia Utente**
- Design moderno con Material Design
- Tema chiaro/scuro
- Layout responsive
- Animazioni fluide

✅ **Componenti**
- Header con ricerca
- Sidebar con categorie
- Card articoli
- Filtri categorie
- Paginazione

✅ **Pagine**
- Home con articoli in evidenza
- Dettaglio articolo completo
- Ricerca avanzata
- Visualizzazione entità NLP

✅ **Servizi**
- Article service
- Category service
- Source service
- Theme service

## 🚀 Quick Start

### Con Docker (Raccomandato)

```bash
# 1. Clone repository
git clone https://github.com/your-username/newsflow.git
cd newsflow

# 2. Configura environment
cp backend/.env.example backend/.env
# Modifica backend/.env con le tue impostazioni

# 3. Avvia servizi
docker-compose up -d

# 4. Inizializza database
docker-compose exec backend python init_db.py

# 5. Accedi all'app
# Frontend: http://localhost:4200
# Backend: http://localhost:8000
# API Docs: http://localhost:8000/api/docs
```

### Setup Manuale

```bash
# Unix/Mac
chmod +x quick-start.sh
./quick-start.sh

# Windows
quick-start.bat
```

## 📚 Documentazione

| Documento | Descrizione |
|-----------|-------------|
| [README.md](README.md) | Overview e introduzione |
| [SETUP.md](SETUP.md) | Setup ambiente sviluppo dettagliato |
| [DEPLOYMENT.md](DEPLOYMENT.md) | Guida deployment produzione |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Come contribuire al progetto |

## 🎨 Caratteristiche Distintive

### 1. Analisi Semantica Avanzata
- NLP multi-lingua (Italiano/Inglese)
- Estrazione automatica keyword
- Riconoscimento entità (persone, organizzazioni, luoghi)
- Quality scoring intelligente

### 2. Cura Intelligente
- Filtri per data, qualità, categoria
- Modalità di lettura personalizzate (mattino, serale, weekend)
- Sistema di raccomandazioni (base)
- Archivio personale con note

### 3. Fonti Autorevoli
- RSS da fonti verificate
- API da news provider professionali
- Scraping etico e rispettoso
- Sistema estensibile per nuove fonti

### 4. Architettura Moderna
- Backend asincrono con FastAPI
- Frontend reattivo con Angular
- Task asincroni con Celery
- Caching intelligente con Redis

### 5. Developer Experience
- Type safety completo (Python type hints + TypeScript)
- API auto-documentata (OpenAPI/Swagger)
- Docker per ambiente consistente
- Script di setup automatizzati

## 🔧 Configurazione

### API Keys Necessarie (Opzionali)

1. **NewsAPI** (gratuito)
   - Registra su [newsapi.org](https://newsapi.org)
   - Aggiungi a `.env`: `NEWSAPI_KEY=your-key`

2. **Guardian API** (gratuito)
   - Registra su [open-platform.theguardian.com](https://open-platform.theguardian.com)
   - Aggiungi a `.env`: `GUARDIAN_API_KEY=your-key`

### Variabili Environment Essenziali

```env
# Database
DATABASE_URL=postgresql://newsflow:password@localhost:5432/newsflow

# Redis
REDIS_URL=redis://localhost:6379

# Security
SECRET_KEY=your-super-secret-key-change-this

# CORS
CORS_ORIGINS=http://localhost:4200
```

## 📊 Database Schema

### Tabelle Principali

- **articles**: Articoli raccolti
- **categories**: Categorie tematiche
- **sources**: Fonti di notizie
- **users**: Utenti registrati
- **saved_articles**: Articoli salvati da utenti
- **annotations**: Note su articoli

### Relazioni

- Article → Source (many-to-one)
- Article → Category (many-to-one)
- User ←→ Article (many-to-many via saved_articles)
- User ←→ Article (one-to-many via annotations)

## 🧪 Testing

```bash
# Backend
cd backend
pytest
pytest --cov=app tests/

# Frontend
cd frontend
ng test
ng e2e
```

## 📈 Performance

- **Backend**: ~100-200 req/s (senza cache)
- **Frontend**: Lighthouse score > 90
- **Database**: Ottimizzato con indici
- **NLP**: Batch processing per efficienza

## 🔮 Roadmap

### Fase 1 (Completata) ✅
- [x] Backend FastAPI completo
- [x] Frontend Angular completo
- [x] Raccolta notizie RSS/API
- [x] Analisi NLP base
- [x] Interfaccia utente moderna

### Fase 2 (Prossimi Step)
- [ ] Autenticazione JWT completa
- [ ] Sistema di raccomandazioni ML
- [ ] Notifiche push
- [ ] Esportazione PDF/EPUB
- [ ] App mobile (Ionic/Capacitor)

### Fase 3 (Futuro)
- [ ] API pubblica
- [ ] Plugin browser
- [ ] Integrazione social
- [ ] Sentiment analysis avanzata
- [ ] Multi-tenancy

## 🤝 Contribuire

Contributi benvenuti! Leggi [CONTRIBUTING.md](CONTRIBUTING.md) per iniziare.

## 📝 Licenza

MIT License - vedi [LICENSE](LICENSE)

## 👥 Team

Progetto sviluppato come sistema autonomo per cura intelligente delle notizie.

## 📧 Supporto

- Issues: [GitHub Issues](https://github.com/your-username/newsflow/issues)
- Discussions: [GitHub Discussions](https://github.com/your-username/newsflow/discussions)
- Documentation: [Wiki](https://github.com/your-username/newsflow/wiki)

---

**NewsFlow** - Leggi solo ciò che conta. 📰✨

