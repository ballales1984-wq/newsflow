# NewsFlow - Intelligent News Curation Platform

NewsFlow è un'applicazione web autonoma per la cura intelligente di notizie da fonti autorevoli, con analisi semantica avanzata e interfaccia personalizzabile.

## 🎯 Caratteristiche Principali

- **Raccolta Automatica**: Aggregazione notizie da fonti selezionate via RSS, API e scraping etico
- **Filtraggio Intelligente**: Selezione per data, qualità semantica e rilevanza tematica
- **Analisi NLP**: Estrazione keyword, classificazione tematica e valutazione pertinenza
- **Categorie**: Tecnologia, Filosofia, Innovazione, Cultura Critica, Cybersecurity
- **Modalità Rituale**: Lettura personalizzata ("mattino", "serale", ecc.)
- **Archivio Personale**: Salvataggio e annotazione articoli
- **Notifiche Intelligenti**: Alert solo per contenuti di alto valore

## 🏗️ Architettura

### Frontend
- **Framework**: Angular 17+
- **UI**: Angular Material
- **State Management**: RxJS + Services
- **HTTP Client**: Angular HttpClient

### Backend
- **Framework**: FastAPI (Python 3.11+)
- **NLP**: spaCy + Hugging Face Transformers
- **Task Queue**: Celery + Redis
- **Caching**: Redis

### Database
- **Primary**: PostgreSQL (dati strutturati)
- **Cache**: Redis (sessioni, cache)

### Deployment
- Frontend: Vercel/Netlify
- Backend: Render/Railway/DigitalOcean
- Database: Supabase/Railway

## 📁 Struttura Progetto

```
newsflow/
├── backend/               # FastAPI application
│   ├── app/
│   │   ├── api/          # API endpoints
│   │   ├── core/         # Configurazione e sicurezza
│   │   ├── models/       # Database models
│   │   ├── schemas/      # Pydantic schemas
│   │   ├── services/     # Business logic
│   │   │   ├── collectors/   # News collectors
│   │   │   ├── nlp/          # NLP analysis
│   │   │   └── filters/      # Content filters
│   │   └── main.py
│   ├── requirements.txt
│   └── .env.example
├── frontend/             # Angular application
│   ├── src/
│   │   ├── app/
│   │   │   ├── components/
│   │   │   ├── services/
│   │   │   ├── models/
│   │   │   └── pages/
│   │   ├── assets/
│   │   └── environments/
│   ├── angular.json
│   └── package.json
└── docker-compose.yml    # Orchestrazione servizi
```

## 🚀 Quick Start

### Prerequisiti
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Redis 7+

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m spacy download it_core_news_lg
python -m spacy download en_core_web_lg
cp .env.example .env
# Configura .env con le tue credenziali
uvicorn app.main:app --reload
```

### Frontend Setup

```bash
cd frontend
npm install
ng serve
```

### Docker Setup (Raccomandato)

```bash
docker-compose up -d
```

## 📚 Fonti Supportate

- MicroMega
- AI4Business
- MIT Technology Review
- Europeana
- Internet Archive
- ICT Security Magazine
- The Guardian (API)
- NewsAPI
- ArXiv
- Medium RSS

## 🔧 Configurazione

### Backend Environment (.env)

```env
DATABASE_URL=postgresql://user:pass@localhost/newsflow
REDIS_URL=redis://localhost:6379
SECRET_KEY=your-secret-key
NEWSAPI_KEY=your-newsapi-key
GUARDIAN_API_KEY=your-guardian-key
```

### Frontend Environment

```typescript
export const environment = {
  production: false,
  apiUrl: 'http://localhost:8000/api/v1'
};
```

## 🎨 Temi e Personalizzazione

L'app supporta temi chiari/scuri e modalità di lettura personalizzate:
- **Mattino**: Focus su aggiornamenti rapidi e novità
- **Serale**: Contenuti di approfondimento e riflessione
- **Weekend**: Long-form e cultura

## 📊 API Endpoints

- `GET /api/v1/articles` - Lista articoli
- `GET /api/v1/articles/{id}` - Dettaglio articolo
- `POST /api/v1/articles/search` - Ricerca semantica
- `GET /api/v1/categories` - Categorie disponibili
- `POST /api/v1/articles/{id}/save` - Salva in archivio
- `POST /api/v1/articles/{id}/annotate` - Aggiungi nota

## 🧪 Testing

```bash
# Backend
cd backend
pytest

# Frontend
cd frontend
ng test
```

## 📦 Deployment

### Backend (Render)
1. Connetti repository GitHub
2. Configura variabili ambiente
3. Deploy automatico da main branch

### Frontend (Vercel)
1. Connetti repository GitHub
2. Configura build command: `ng build`
3. Output directory: `dist/frontend`

## 🤝 Contribuire

Questo è un progetto autonomo e open-source. Contributi benvenuti!

## 📝 Licenza

MIT License - vedi LICENSE file

## 🔮 Roadmap

- [ ] Integrazione più fonti RSS
- [ ] Supporto multilingua completo
- [ ] App mobile (Ionic/Capacitor)
- [ ] Condivisione articoli social
- [ ] Esportazione PDF/EPUB
- [ ] Plugin browser
- [ ] API pubblica

## 📧 Contatti

Per domande e supporto, apri una issue su GitHub.

---

**NewsFlow** - Leggi solo ciò che conta.

