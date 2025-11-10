# NewsFlow - Guida al Deployment

Questa guida fornisce istruzioni dettagliate per il deployment di NewsFlow in produzione.

## 📋 Prerequisiti

- Account GitHub (per il repository)
- Account Vercel/Netlify (per il frontend)
- Account Render/Railway (per il backend)
- Account Supabase/Railway (per PostgreSQL)
- Account Upstash/Redis Cloud (per Redis)

## 🚀 Deployment Backend (Render)

### 1. Preparazione Repository

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/your-username/newsflow.git
git push -u origin main
```

### 2. Setup Database PostgreSQL

**Opzione A: Railway**

1. Vai su [railway.app](https://railway.app)
2. Crea nuovo progetto
3. Aggiungi PostgreSQL
4. Copia il `DATABASE_URL`

**Opzione B: Supabase**

1. Vai su [supabase.com](https://supabase.com)
2. Crea nuovo progetto
3. Vai su Settings > Database
4. Copia la connection string

### 3. Setup Redis

**Render Redis** (raccomandato)

1. Su Render, crea un nuovo Redis instance
2. Copia il `REDIS_URL`

**Upstash**

1. Vai su [upstash.com](https://upstash.com)
2. Crea nuovo database Redis
3. Copia l'URL di connessione

### 4. Deploy Backend su Render

1. Vai su [render.com](https://render.com)
2. Crea nuovo **Web Service**
3. Connetti il repository GitHub
4. Configura:
   - **Name**: newsflow-backend
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt && python -m spacy download it_core_news_lg && python -m spacy download en_core_web_lg`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: Starter ($7/month)

5. Aggiungi variabili ambiente:

```env
DATABASE_URL=<your-postgresql-url>
REDIS_URL=<your-redis-url>
SECRET_KEY=<generate-strong-key>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
CORS_ORIGINS=https://your-frontend-domain.vercel.app
NEWSAPI_KEY=<your-newsapi-key>
GUARDIAN_API_KEY=<your-guardian-key>
SIMILARITY_THRESHOLD=0.7
MIN_ARTICLE_LENGTH=200
MAX_ARTICLE_AGE_DAYS=30
COLLECTION_INTERVAL_HOURS=1
MAX_ARTICLES_PER_SOURCE=50
```

6. Deploy!

### 5. Inizializza Database

Dopo il primo deploy, esegui:

```bash
# Connettiti via SSH o usa Render Shell
python init_db.py
```

### 6. Setup Celery Workers (opzionale)

Per i task in background, crea servizi separati su Render:

**Celery Worker**
- Command: `celery -A app.core.celery_app worker --loglevel=info`

**Celery Beat**
- Command: `celery -A app.core.celery_app beat --loglevel=info`

## 🌐 Deployment Frontend (Vercel)

### 1. Build di Produzione Locale (test)

```bash
cd frontend
npm install
ng build --configuration production
```

### 2. Deploy su Vercel

**Via Vercel CLI**

```bash
npm install -g vercel
cd frontend
vercel
```

**Via Dashboard Vercel**

1. Vai su [vercel.com](https://vercel.com)
2. Importa progetto da GitHub
3. Configura:
   - **Framework**: Angular
   - **Root Directory**: `frontend`
   - **Build Command**: `ng build`
   - **Output Directory**: `dist/newsflow`

4. Aggiungi variabili ambiente:

```env
PRODUCTION=true
```

5. Deploy!

### 3. Configurazione Dominio Custom (opzionale)

1. Su Vercel, vai su Settings > Domains
2. Aggiungi il tuo dominio
3. Configura DNS secondo le istruzioni

## 🐳 Deployment con Docker (Alternativa)

### 1. Build e Push Immagini

```bash
# Backend
docker build -t your-registry/newsflow-backend:latest ./backend
docker push your-registry/newsflow-backend:latest

# Frontend
docker build -t your-registry/newsflow-frontend:latest ./frontend
docker push your-registry/newsflow-frontend:latest
```

### 2. Deploy su VPS

Su un VPS (DigitalOcean, Linode, etc.):

```bash
# Clona repository
git clone https://github.com/your-username/newsflow.git
cd newsflow

# Configura .env
cp backend/.env.example backend/.env
# Modifica backend/.env con le tue credenziali

# Avvia con Docker Compose
docker-compose up -d

# Inizializza database
docker-compose exec backend python init_db.py
```

### 3. Setup Nginx Reverse Proxy

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location / {
        proxy_pass http://localhost:4200;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 4. SSL con Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

## 🔐 Sicurezza

### 1. Genera SECRET_KEY Sicura

```python
import secrets
print(secrets.token_urlsafe(32))
```

### 2. Configura CORS Correttamente

Assicurati che `CORS_ORIGINS` contenga solo i domini autorizzati.

### 3. Rate Limiting

Considera l'uso di servizi come Cloudflare per proteggere le API.

## 📊 Monitoring

### 1. Backend Monitoring

**Render**
- Dashboard integrato con logs e metriche

**Sentry** (errori)
```bash
pip install sentry-sdk
```

```python
# In app/main.py
import sentry_sdk
sentry_sdk.init(dsn="your-sentry-dsn")
```

### 2. Frontend Monitoring

**Vercel Analytics**
- Abilitato automaticamente

**Google Analytics**
```typescript
// In index.html
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
```

## 🔄 CI/CD

### GitHub Actions

Crea `.github/workflows/deploy.yml`:

```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Render
        run: |
          curl -X POST ${{ secrets.RENDER_DEPLOY_HOOK }}

  deploy-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Vercel
        run: |
          npm install -g vercel
          cd frontend
          vercel --prod --token=${{ secrets.VERCEL_TOKEN }}
```

## 🧪 Testing in Produzione

```bash
# Test backend
curl https://your-backend.onrender.com/api/health

# Test frontend
curl https://your-frontend.vercel.app
```

## 📝 Backup

### Database Backup (automatico)

**Railway/Supabase**
- Backup automatici inclusi

**Render**
- Configura backup giornalieri nel dashboard

### Manual Backup

```bash
# PostgreSQL
pg_dump $DATABASE_URL > backup_$(date +%Y%m%d).sql

# Restore
psql $DATABASE_URL < backup_20240101.sql
```

## 🎯 Checklist Pre-Deployment

- [ ] Tutte le variabili ambiente configurate
- [ ] SECRET_KEY generata e sicura
- [ ] Database PostgreSQL pronto
- [ ] Redis configurato
- [ ] CORS configurato correttamente
- [ ] API keys (NewsAPI, Guardian) ottenute
- [ ] Modelli spaCy scaricati
- [ ] Database inizializzato con `init_db.py`
- [ ] SSL/HTTPS abilitato
- [ ] Monitoring configurato
- [ ] Backup automatici attivi

## 🆘 Troubleshooting

### Errore: "Module not found"
```bash
# Reinstalla dipendenze
pip install -r requirements.txt --force-reinstall
```

### Errore: "Database connection failed"
```bash
# Verifica DATABASE_URL
echo $DATABASE_URL
# Testa connessione
psql $DATABASE_URL
```

### Errore: "spaCy models not found"
```bash
# Scarica modelli manualmente
python -m spacy download it_core_news_lg
python -m spacy download en_core_web_lg
```

## 📞 Supporto

Per problemi o domande:
- Apri una issue su GitHub
- Consulta la documentazione ufficiale dei servizi utilizzati

---

**NewsFlow** - Deploy con successo! 🚀

