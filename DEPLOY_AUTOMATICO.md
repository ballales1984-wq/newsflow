# 🚀 Deploy Automatico su Render - Guida Rapida

## ✅ Tutto Pronto per il Deploy!

Il sistema è configurato per aggiornare automaticamente gli articoli **OGNI 4 ORE**.

## 📦 Cosa Include

- 🌐 **Backend API** - FastAPI su porta pubblica
- 👷 **Celery Worker** - Elabora task in background
- ⏰ **Celery Beat** - Scheduler automatico (ogni 4 ore!)
- 💾 **PostgreSQL** - Database (piano gratuito)
- 🔴 **Redis** - Cache e message broker (piano gratuito)

## 🎯 Deploy in 3 Click

### 1️⃣ Vai su Render.com

Apri: https://render.com

### 2️⃣ Connetti GitHub

1. Clicca **"New +"** → **"Blueprint"**
2. Connetti il repo: `ballales1984-wq/newsflow`
3. Render rileva automaticamente `render.yaml`

### 3️⃣ Deploy!

Clicca **"Apply"** e aspetta ~5 minuti

## ✨ Cosa Succede Automaticamente

Render crea:

```
✅ newsflow-backend      → API Backend (Web Service)
✅ newsflow-worker       → Celery Worker (Background)
✅ newsflow-beat         → Scheduler (ogni 4 ore)
✅ newsflow-db           → PostgreSQL Database
✅ newsflow-redis        → Redis Cache
```

## ⏰ Schedule Aggiornamenti

Gli articoli si aggiorneranno automaticamente:

- 🕛 **00:00** - Mezzanotte
- 🕓 **04:00** - Mattina presto
- 🕗 **08:00** - Mattina
- 🕛 **12:00** - Mezzogiorno
- 🕓 **16:00** - Pomeriggio
- 🕗 **20:00** - Sera

## 🔗 Configurazione Frontend

Dopo il deploy, aggiorna l'URL del backend nel frontend:

1. Vai su **Vercel Dashboard**
2. Apri progetto **newsflow**
3. **Settings** → **Environment Variables**
4. Modifica `API_URL`:

```
VITE_API_URL=https://newsflow-backend.onrender.com
```

oppure nel file `frontend/src/environments/environment.prod.ts`:

```typescript
export const environment = {
  production: true,
  apiUrl: 'https://newsflow-backend.onrender.com/api/v1'
};
```

## 🎛️ Monitoraggio

### Dashboard Render

Vai su https://dashboard.render.com per vedere:

- 📊 **Logs** di ogni servizio
- 💻 **Metriche** CPU/Memoria
- ⚡ **Status** dei worker
- 🔄 **Deploy History**

### Verificare che funzioni

Dopo il deploy, testa:

```bash
# API Backend
curl https://newsflow-backend.onrender.com/api/v1/articles

# Categorie (con le nuove!)
curl https://newsflow-backend.onrender.com/api/v1/categories
```

### Log Celery Beat

Vai su Dashboard → **newsflow-beat** → **Logs**

Dovresti vedere:

```
[INFO] Scheduler: Sending due task collect-news-every-4-hours
[INFO] Task app.services.tasks.collect_all_news[...] received
[INFO] Collected 156 articles from 7 sources
```

## 🆓 Piano Gratuito

Tutto **GRATIS** con Render Free Plan:

- ✅ 750 ore/mese di compute (sufficiente per 3 servizi 24/7)
- ✅ PostgreSQL 1GB
- ✅ Redis 25MB
- ✅ Deploy automatici da GitHub
- ✅ SSL certificati automatici
- ⚠️ Auto-sleep dopo 15 min di inattività (solo web service)

**Nota**: I worker (celery-worker e celery-beat) NON vanno in sleep!

## 🔄 Aggiornamenti Futuri

Quando fai push su GitHub, Render fa **auto-deploy**:

```bash
git add .
git commit -m "Aggiunte nuove fonti RSS"
git push origin main
```

→ Render rebuilda e deploya automaticamente! 🚀

## 🐛 Troubleshooting

### Worker non parte

```
Logs → newsflow-worker → cerca "ERROR"
```

Possibili cause:
- Redis non connesso
- Dipendenze mancanti
- Variabili d'ambiente sbagliate

### Database non inizializzato

Dopo il primo deploy, esegui:

```bash
# Nel dashboard Render → Shell del backend
python -c "from app.core.database import Base, engine; Base.metadata.create_all(bind=engine)"
python init_db.py
```

### Articoli non si aggiornano

1. Verifica che **newsflow-beat** sia attivo
2. Controlla i log di **newsflow-beat**
3. Verifica che Redis sia connesso

## 📞 Support

- 📧 Render Support: https://render.com/docs
- 💬 Community: https://community.render.com
- 📖 Docs: https://render.com/docs/deploys

---

## 🎉 Pronto!

Dopo il deploy, il tuo NewsFlow sarà:

✅ Online 24/7
✅ Aggiornato ogni 4 ore automaticamente
✅ Scalabile e performante
✅ GRATIS! 

**URL del tuo backend**: `https://newsflow-backend.onrender.com`

Buon lancio! 🚀📰

