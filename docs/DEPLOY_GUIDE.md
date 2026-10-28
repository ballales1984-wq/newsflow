# 🚀 NewsFlow - Guida Deploy Rapida

## ✅ Testing Locale

### Test Backend

```bash
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
pytest -v
```

### Test Frontend

```bash
cd frontend
npm run test -- --watch=false
```

### Test Completo Automatico

```bash
# Unix/Mac/Git Bash
./test-local.sh

# Windows PowerShell
# Esegui i comandi sopra manualmente
```

---

## 🌐 Deploy Backend (Render)

### 1. Prepara Repository GitHub

```bash
git init
git add .
git commit -m "Initial commit: NewsFlow"
git branch -M main
git remote add origin https://github.com/your-username/newsflow.git
git push -u origin main
```

### 2. Crea Database PostgreSQL

**Opzione A: Railway** (Raccomandato)
1. Vai su https://railway.app
2. "New Project" → "Provision PostgreSQL"
3. Copia `DATABASE_URL` dalle variabili

**Opzione B: Render**
1. Dashboard Render → "New" → "PostgreSQL"
2. Nome: `newsflow-db`
3. Copia "Internal Database URL"

### 3. Crea Redis Instance

**Su Render:**
1. "New" → "Redis"
2. Nome: `newsflow-redis`
3. Copia "Internal Redis URL"

### 4. Deploy Backend su Render

1. Dashboard → "New" → "Web Service"
2. Connetti repository GitHub
3. Configura:

```yaml
Name: newsflow-backend
Root Directory: backend
Build Command: pip install -r requirements.txt && python -m spacy download it_core_news_lg && python -m spacy download en_core_web_lg
Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
Instance Type: Starter
```

4. **Environment Variables**:

```env
DATABASE_URL=<your-postgresql-internal-url>
REDIS_URL=<your-redis-internal-url>
SECRET_KEY=<generate-with-python-secrets>
ALGORITHM=HS256
CORS_ORIGINS=https://your-frontend.vercel.app
NEWSAPI_KEY=<optional>
GUARDIAN_API_KEY=<optional>
```

5. Clicca "Create Web Service"

### 5. Inizializza Database

Dopo primo deploy, vai su Render → Shell:

```bash
python init_db.py
```

---

## 🎨 Deploy Frontend (Vercel)

### 1. Installa Vercel CLI (opzionale)

```bash
npm install -g vercel
```

### 2. Deploy via Dashboard

1. Vai su https://vercel.com
2. "New Project" → Importa da GitHub
3. Seleziona repository `newsflow`
4. Configura:

```yaml
Framework Preset: Angular
Root Directory: frontend
Build Command: npm run build -- --configuration production
Output Directory: dist/newsflow
```

5. **Environment Variables**:

```env
PRODUCTION=true
```

6. Clicca "Deploy"

### 3. Deploy via CLI (Alternativo)

```bash
cd frontend
vercel

# Per produzione
vercel --prod
```

### 4. Configura Backend URL

Dopo deploy backend, aggiorna in Vercel:

1. Project Settings → Environment Variables
2. Aggiungi:
   - `API_URL` = `https://newsflow-backend.onrender.com/api/v1`

3. Redeploy:

```bash
vercel --prod
```

---

## 🐳 Deploy con Docker (VPS)

### Su DigitalOcean/Linode/etc:

```bash
# 1. SSH nel server
ssh root@your-server-ip

# 2. Installa Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# 3. Clone repository
git clone https://github.com/your-username/newsflow.git
cd newsflow

# 4. Configura .env
nano backend/.env
# Inserisci le variabili

# 5. Avvia servizi
docker-compose up -d

# 6. Inizializza DB
docker-compose exec backend python init_db.py

# 7. Setup Nginx (opzionale)
# Vedi DEPLOYMENT.md per config completa
```

---

## ✨ Verifica Deploy

### Backend

```bash
curl https://your-backend.onrender.com/api/health
# Deve rispondere: {"status":"healthy"}
```

### Frontend

```bash
curl https://your-frontend.vercel.app
# Deve rispondere con HTML
```

### API Docs

Apri: `https://your-backend.onrender.com/api/docs`

---

## 🎯 Checklist Post-Deploy

- [ ] Backend risponde su `/api/health`
- [ ] Frontend carica correttamente
- [ ] Database popolato con categorie/fonti
- [ ] API docs accessibili
- [ ] CORS configurato correttamente
- [ ] SSL/HTTPS attivo
- [ ] Variabili ambiente settate
- [ ] Logs senza errori critici

---

## 🔄 Deploy Aggiornamenti

### Automatico (Git push)

```bash
git add .
git commit -m "Update: descrizione"
git push origin main

# Render e Vercel deploieranno automaticamente
```

### Manuale

```bash
# Script automatico
./deploy.sh

# O manualmente
cd frontend
vercel --prod
```

---

## 📊 Monitoring

### Render
- Dashboard → Logs
- Dashboard → Metrics

### Vercel
- Dashboard → Deployments
- Analytics automatico

### Uptime Monitoring (Gratuiti)
- UptimeRobot: https://uptimerobot.com
- Pingdom: https://www.pingdom.com (free tier)

---

## 🆘 Troubleshooting

### Backend non si avvia

```bash
# Controlla logs su Render
# Verifica variabili ambiente
# Controlla DATABASE_URL e REDIS_URL
```

### Frontend non connette al backend

```bash
# Verifica CORS_ORIGINS nel backend
# Controlla API_URL nel frontend
# Testa endpoint: curl https://backend-url/api/health
```

### Database vuoto

```bash
# Su Render Shell
python init_db.py
```

---

## 🎉 Success!

Una volta completato:

✅ Backend: `https://newsflow-backend.onrender.com`  
✅ Frontend: `https://newsflow.vercel.app`  
✅ API Docs: `https://newsflow-backend.onrender.com/api/docs`

**Il tuo NewsFlow è live!** 🚀

---

## 📞 Supporto

- Issues: GitHub Issues
- Docs: README.md, DEPLOYMENT.md
- Discord: (crea server se vuoi community)

---

**Tempo stimato totale: 30-45 minuti** ⏱️

