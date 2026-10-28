# NewsFlow - Setup Guide

Guida completa per configurare l'ambiente di sviluppo locale.

## 📋 Requisiti di Sistema

- **Python**: 3.11 o superiore
- **Node.js**: 18.x o superiore
- **PostgreSQL**: 15 o superiore
- **Redis**: 7 o superiore
- **Git**: Per il version control

## 🔧 Setup Backend

### 1. Clona il Repository

```bash
git clone https://github.com/your-username/newsflow.git
cd newsflow
```

### 2. Setup Python Virtual Environment

```bash
cd backend

# Crea virtual environment
python -m venv venv

# Attiva virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

### 3. Installa Dipendenze Python

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Scarica Modelli NLP

```bash
# Modello Italiano
python -m spacy download it_core_news_lg

# Modello Inglese
python -m spacy download en_core_web_lg
```

### 5. Setup Database PostgreSQL

**Opzione A: Installazione Locale**

```bash
# Windows (con chocolatey)
choco install postgresql

# Mac (con homebrew)
brew install postgresql@15

# Linux (Ubuntu/Debian)
sudo apt update
sudo apt install postgresql postgresql-contrib
```

**Crea Database:**

```bash
# Accedi a PostgreSQL
psql -U postgres

# Crea database e utente
CREATE DATABASE newsflow;
CREATE USER newsflow WITH PASSWORD 'newsflow_password';
GRANT ALL PRIVILEGES ON DATABASE newsflow TO newsflow;
\q
```

**Opzione B: Docker**

```bash
docker run --name newsflow-postgres \
  -e POSTGRES_USER=newsflow \
  -e POSTGRES_PASSWORD=newsflow_password \
  -e POSTGRES_DB=newsflow \
  -p 5432:5432 \
  -d postgres:15-alpine
```

### 6. Setup Redis

**Opzione A: Installazione Locale**

```bash
# Windows (con chocolatey)
choco install redis-64

# Mac (con homebrew)
brew install redis

# Linux (Ubuntu/Debian)
sudo apt install redis-server
```

**Avvia Redis:**

```bash
redis-server
```

**Opzione B: Docker**

```bash
docker run --name newsflow-redis \
  -p 6379:6379 \
  -d redis:7-alpine
```

### 7. Configura Environment Variables

```bash
# Copia template
cp .env.example .env

# Modifica .env con i tuoi valori
```

Esempio `.env`:

```env
DATABASE_URL=postgresql://newsflow:newsflow_password@localhost:5432/newsflow
REDIS_URL=redis://localhost:6379
SECRET_KEY=your-super-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
CORS_ORIGINS=http://localhost:4200
NEWSAPI_KEY=your-newsapi-key
GUARDIAN_API_KEY=your-guardian-key
SIMILARITY_THRESHOLD=0.7
MIN_ARTICLE_LENGTH=200
MAX_ARTICLE_AGE_DAYS=30
COLLECTION_INTERVAL_HOURS=1
MAX_ARTICLES_PER_SOURCE=50
```

### 8. Inizializza Database

```bash
# Crea tabelle e dati iniziali
python init_db.py
```

### 9. Avvia Backend

```bash
# Development server con auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Il backend sarà disponibile su: `http://localhost:8000`

API Documentation: `http://localhost:8000/api/docs`

### 10. Avvia Celery Workers (Opzionale)

**Terminale 2:**
```bash
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
celery -A app.core.celery_app worker --loglevel=info
```

**Terminale 3:**
```bash
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
celery -A app.core.celery_app beat --loglevel=info
```

## 🎨 Setup Frontend

### 1. Installa Dipendenze Node

```bash
cd frontend
npm install
```

### 2. Configura Environment

Il file `src/environments/environment.ts` è già configurato per lo sviluppo locale.

Se necessario, modifica l'URL del backend:

```typescript
export const environment = {
  production: false,
  apiUrl: 'http://localhost:8000/api/v1'
};
```

### 3. Avvia Frontend

```bash
npm start
# oppure
ng serve
```

Il frontend sarà disponibile su: `http://localhost:4200`

## 🐳 Setup con Docker (Tutto in Uno)

### 1. Prerequisiti

- Docker Desktop installato
- Docker Compose disponibile

### 2. Avvia Tutti i Servizi

```bash
# Dalla root del progetto
docker-compose up -d
```

Questo avvierà:
- PostgreSQL su porta 5432
- Redis su porta 6379
- Backend su porta 8000
- Frontend su porta 4200
- Celery Worker
- Celery Beat

### 3. Inizializza Database

```bash
docker-compose exec backend python init_db.py
```

### 4. Visualizza Logs

```bash
# Tutti i servizi
docker-compose logs -f

# Servizio specifico
docker-compose logs -f backend
```

### 5. Ferma Servizi

```bash
docker-compose down
```

## 🔑 API Keys (Opzionali ma Raccomandati)

### NewsAPI

1. Vai su [newsapi.org](https://newsapi.org)
2. Registrati gratuitamente
3. Copia la tua API key
4. Aggiungi a `.env`: `NEWSAPI_KEY=your-key`

### The Guardian API

1. Vai su [open-platform.theguardian.com](https://open-platform.theguardian.com)
2. Registrati per un API key
3. Copia la tua API key
4. Aggiungi a `.env`: `GUARDIAN_API_KEY=your-key`

## ✅ Verifica Installazione

### Backend

```bash
# Test health endpoint
curl http://localhost:8000/api/health

# Test articles endpoint
curl http://localhost:8000/api/v1/articles

# Apri API docs
# Browser: http://localhost:8000/api/docs
```

### Frontend

```bash
# Apri nel browser
# http://localhost:4200
```

## 🧪 Testing

### Backend Tests

```bash
cd backend
pytest
```

### Frontend Tests

```bash
cd frontend
ng test
```

## 📝 Comandi Utili

### Backend

```bash
# Attiva virtual environment
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Installa nuova dipendenza
pip install package-name
pip freeze > requirements.txt

# Formatta codice
black app/
flake8 app/

# Database migrations (con Alembic)
alembic revision --autogenerate -m "description"
alembic upgrade head
```

### Frontend

```bash
# Genera componente
ng generate component components/component-name

# Genera servizio
ng generate service services/service-name

# Build di produzione
ng build --configuration production

# Lint
ng lint
```

### Docker

```bash
# Rebuild dopo modifiche
docker-compose up -d --build

# Rimuovi volumi
docker-compose down -v

# Accedi a container
docker-compose exec backend bash
docker-compose exec frontend sh
```

## 🐛 Troubleshooting

### Problema: Port già in uso

```bash
# Trova processo sulla porta 8000
# Linux/Mac:
lsof -ti:8000 | xargs kill -9
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Problema: Database connection refused

```bash
# Verifica che PostgreSQL sia in esecuzione
# Linux:
sudo systemctl status postgresql
# Mac:
brew services list
# Windows:
services.msc (cerca PostgreSQL)

# Test connessione
psql -h localhost -U newsflow -d newsflow
```

### Problema: Redis connection refused

```bash
# Verifica che Redis sia in esecuzione
redis-cli ping
# Dovrebbe rispondere: PONG
```

### Problema: Moduli Python mancanti

```bash
pip install -r requirements.txt --force-reinstall
```

### Problema: Angular build errors

```bash
# Pulisci cache
rm -rf node_modules package-lock.json
npm install

# O con npm ci (clean install)
npm ci
```

## 📚 Risorse Aggiuntive

- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [Angular Documentation](https://angular.io/docs)
- [spaCy Documentation](https://spacy.io/usage)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Redis Documentation](https://redis.io/documentation)

## 🎓 Prossimi Passi

1. ✅ Completa setup ambiente di sviluppo
2. 📖 Leggi `README.md` per panoramica progetto
3. 🚀 Consulta `DEPLOYMENT.md` per il deployment
4. 💡 Esplora API su `http://localhost:8000/api/docs`
5. 🎨 Personalizza frontend in `frontend/src/app`
6. 🔧 Aggiungi nuove fonti RSS in `backend/init_db.py`

## ❓ Supporto

Per problemi durante il setup:
1. Controlla questa guida
2. Consulta la documentazione ufficiale
3. Apri una issue su GitHub

---

**Buon coding!** 🚀

