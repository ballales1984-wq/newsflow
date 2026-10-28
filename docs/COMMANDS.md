# NewsFlow - Comandi Utili

Riferimento rapido per i comandi più utilizzati durante lo sviluppo.

## 🐳 Docker

```bash
# Avvia tutti i servizi
docker-compose up -d

# Avvia con logs
docker-compose up

# Stop servizi
docker-compose down

# Stop e rimuovi volumi
docker-compose down -v

# Rebuild dopo modifiche
docker-compose up -d --build

# Visualizza logs
docker-compose logs -f
docker-compose logs -f backend

# Accedi a container
docker-compose exec backend bash
docker-compose exec postgres psql -U newsflow

# Riavvia servizio specifico
docker-compose restart backend
```

## 🐍 Backend

### Setup

```bash
cd backend

# Crea virtual environment
python -m venv venv

# Attiva venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Installa dipendenze
pip install -r requirements.txt

# Scarica modelli NLP
python -m spacy download it_core_news_lg
python -m spacy download en_core_web_lg
```

### Development

```bash
# Avvia server development
uvicorn app.main:app --reload

# Con host e porta custom
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Inizializza database
python init_db.py

# Avvia Celery worker
celery -A app.core.celery_app worker --loglevel=info

# Avvia Celery beat
celery -A app.core.celery_app beat --loglevel=info

# Trigger raccolta manuale (in Python)
python -c "from app.services.tasks import collect_all_news; collect_all_news()"
```

### Database

```bash
# Accedi a PostgreSQL
psql postgresql://newsflow:newsflow_password@localhost:5432/newsflow

# Query utili
psql newsflow -c "SELECT COUNT(*) FROM articles;"
psql newsflow -c "SELECT * FROM categories;"
psql newsflow -c "SELECT name, last_collected_at FROM sources;"

# Backup database
pg_dump newsflow > backup.sql

# Restore database
psql newsflow < backup.sql

# Reset database (ATTENZIONE: cancella tutto!)
psql newsflow -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
python init_db.py
```

### Testing

```bash
# Run tutti i test
pytest

# Con coverage
pytest --cov=app tests/

# Test specifico
pytest tests/test_articles.py

# Test con output verbose
pytest -v

# Stop al primo errore
pytest -x
```

### Code Quality

```bash
# Format con Black
black app/

# Check style con Flake8
flake8 app/

# Type checking con mypy
mypy app/

# Tutto insieme
black app/ && flake8 app/ && mypy app/ && pytest
```

## 🎨 Frontend

### Setup

```bash
cd frontend

# Installa dipendenze
npm install

# Clean install
npm ci
```

### Development

```bash
# Avvia dev server
npm start
# oppure
ng serve

# Con host custom
ng serve --host 0.0.0.0 --port 4200

# Con auto-open browser
ng serve --open
```

### Build

```bash
# Build development
ng build

# Build production
ng build --configuration production

# Build e analizza bundle
ng build --stats-json
npx webpack-bundle-analyzer dist/newsflow/stats.json
```

### Generate

```bash
# Nuovo componente
ng generate component components/nome-componente
ng g c components/nome-componente

# Nuovo servizio
ng generate service services/nome-servizio
ng g s services/nome-servizio

# Nuovo modulo
ng generate module modules/nome-modulo
ng g m modules/nome-modulo

# Con routing
ng g m modules/nome-modulo --routing
```

### Testing

```bash
# Unit tests
ng test

# Con coverage
ng test --code-coverage

# Single run (no watch)
ng test --watch=false

# E2E tests
ng e2e
```

### Code Quality

```bash
# Lint
ng lint

# Fix automatico
ng lint --fix
```

## 🗄️ Database Management

### PostgreSQL

```bash
# Connessione
psql -h localhost -U newsflow -d newsflow

# Liste
\dt              # Lista tabelle
\d articles      # Descrive tabella
\l               # Lista databases
\du              # Lista utenti

# Query utili
SELECT COUNT(*) FROM articles;
SELECT COUNT(*) FROM articles WHERE published_at > NOW() - INTERVAL '7 days';
SELECT c.name, COUNT(a.id) FROM categories c LEFT JOIN articles a ON c.id = a.category_id GROUP BY c.name;

# Performance
EXPLAIN ANALYZE SELECT * FROM articles WHERE category_id = 1;
```

### Redis

```bash
# Connessione
redis-cli

# Comandi base
PING                    # Test connessione
KEYS *                  # Lista chiavi (dev only!)
GET key                 # Get valore
SET key value           # Set valore
DEL key                 # Elimina chiave
FLUSHDB                 # Cancella tutto (ATTENZIONE!)

# Info
INFO                    # Info server
DBSIZE                  # Numero chiavi
MEMORY USAGE key        # Memory di una chiave
```

## 🔍 Debugging

### Backend

```bash
# Con debugger
python -m pdb app/main.py

# Con iPython
ipython
>>> from app.services.nlp import NLPAnalyzer
>>> analyzer = NLPAnalyzer()
>>> analyzer.analyze("Test text")

# Logs
tail -f logs/app.log

# Celery task status
celery -A app.core.celery_app inspect active
celery -A app.core.celery_app inspect stats
```

### Frontend

```bash
# Source maps per debugging
ng build --source-map

# Lighthouse audit
npm install -g @lhci/cli
lhci autorun

# Bundle analyzer
npm install -g webpack-bundle-analyzer
ng build --stats-json
webpack-bundle-analyzer dist/newsflow/stats.json
```

## 📦 Dependencies

### Backend

```bash
# Aggiungi dipendenza
pip install package-name
pip freeze > requirements.txt

# Aggiorna dipendenza
pip install --upgrade package-name

# Rimuovi dipendenza
pip uninstall package-name
```

### Frontend

```bash
# Aggiungi dipendenza
npm install package-name
npm install --save-dev package-name  # dev dependency

# Aggiorna dipendenze
npm update

# Controlla outdated
npm outdated

# Audit sicurezza
npm audit
npm audit fix
```

## 🔄 Git Workflow

```bash
# Nuovo branch
git checkout -b feature/nome-feature

# Commit
git add .
git commit -m "feat: descrizione"

# Push
git push origin feature/nome-feature

# Sync con main
git checkout main
git pull origin main
git checkout feature/nome-feature
git rebase main

# Squash commits
git rebase -i HEAD~3
```

## 🚀 Deployment

### Backend (Render)

```bash
# Deploy via git push
git push render main

# Via Render CLI
render deploy
```

### Frontend (Vercel)

```bash
# Deploy
vercel

# Deploy production
vercel --prod

# Alias
vercel alias
```

## 📊 Monitoring

### Logs

```bash
# Docker logs
docker-compose logs -f backend

# Render logs
render logs

# Vercel logs
vercel logs
```

### Performance

```bash
# Backend load test
pip install locust
locust -f tests/load_test.py

# Frontend performance
npm install -g lighthouse
lighthouse http://localhost:4200
```

## 🔧 Maintenance

### Cleanup

```bash
# Python cache
find . -type d -name "__pycache__" -exec rm -r {} +
find . -type f -name "*.pyc" -delete

# Node modules
rm -rf node_modules package-lock.json
npm install

# Docker
docker system prune -a
docker volume prune
```

### Backup

```bash
# Database backup
pg_dump newsflow > backup_$(date +%Y%m%d_%H%M%S).sql

# Code backup
tar -czf newsflow_backup_$(date +%Y%m%d).tar.gz \
  --exclude='node_modules' \
  --exclude='venv' \
  --exclude='__pycache__' \
  .
```

## ⚡ Quick Commands

```bash
# Full restart (Docker)
docker-compose down && docker-compose up -d && docker-compose logs -f

# Backend restart
cd backend && source venv/bin/activate && uvicorn app.main:app --reload

# Frontend restart
cd frontend && npm start

# Rebuild tutto
docker-compose down -v && docker-compose up -d --build
```

## 🆘 Troubleshooting

```bash
# Port già in uso
lsof -ti:8000 | xargs kill -9  # Mac/Linux
netstat -ano | findstr :8000   # Windows

# Permessi script
chmod +x quick-start.sh

# Reset completo
docker-compose down -v
rm -rf backend/venv frontend/node_modules
# Poi ri-setup
```

---

💡 **Tip**: Crea alias per comandi frequenti nel tuo `.bashrc` o `.zshrc`!

