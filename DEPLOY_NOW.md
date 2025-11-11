# 🚀 DEPLOY RAPIDO - Guida Passo Passo

## ✅ FATTO:
- [x] Codice completo creato
- [x] Git inizializzato
- [x] Primo commit fatto
- [x] Frontend testato e funzionante

## 📋 PROSSIMI PASSI:

### 1. Push su GitHub

```bash
# Aggiungi remote (sostituisci con il tuo URL)
git remote add origin https://github.com/TUO-USERNAME/newsflow.git

# Push del codice
git branch -M main
git push -u origin main
```

### 2. Deploy Frontend su Vercel

1. Vai su https://vercel.com
2. "Add New Project"
3. Importa da GitHub → Seleziona `newsflow`
4. Configura:
   - **Framework Preset**: Angular
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build -- --configuration production`
   - **Output Directory**: `dist/newsflow`
5. Clicca "Deploy"

⏱️ **Tempo: 2-3 minuti**

### 3. Deploy Backend su Render

1. Vai su https://render.com
2. "New" → "Web Service"
3. Connetti GitHub → Seleziona `newsflow`
4. Configura:
   - **Name**: `newsflow-backend`
   - **Root Directory**: `backend`
   - **Build Command**: 
     ```
     pip install -r requirements.txt && python -m spacy download it_core_news_lg && python -m spacy download en_core_web_lg
     ```
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: Free

5. **Environment Variables** (clicca "Advanced"):
   ```
   DATABASE_URL=postgresql://...  (Render lo crea automaticamente)
   REDIS_URL=redis://...  (Render lo crea automaticamente)
   SECRET_KEY=<genera-una-chiave-casuale>
   CORS_ORIGINS=https://tuo-frontend.vercel.app
   ```

6. Clicca "Create Web Service"

⏱️ **Tempo: 5-10 minuti** (prima build)

### 4. Crea Database PostgreSQL su Render

1. Dashboard Render → "New" → "PostgreSQL"
2. Name: `newsflow-db`
3. Clicca "Create Database"
4. Copia "Internal Database URL"
5. Aggiorna `DATABASE_URL` nel backend
6. Aspetta che backend redeploy

### 5. Inizializza Database

Quando backend è online:
1. Vai su Render → Il tuo service → "Shell"
2. Esegui: `python init_db.py`

Questo popola categorie e fonti!

### 6. Collega Frontend a Backend

Su Vercel:
1. Settings → Environment Variables
2. Aggiungi:
   - `API_URL` = `https://tuo-backend.onrender.com/api/v1`
3. Redeploy

### 7. DONE! 🎉

Vai su: `https://tuo-frontend.vercel.app`

Vedrai:
- ✅ Interfaccia completa
- ✅ Categorie popolate
- ✅ Fonti RSS configurate
- ✅ Sistema di raccolta attivo!

---

## 🐛 Troubleshooting

**Backend non si avvia?**
- Controlla logs su Render
- Verifica variabili ambiente
- Controlla che DATABASE_URL sia corretto

**Frontend errore connessione?**
- Verifica CORS_ORIGINS nel backend
- Verifica API_URL nel frontend
- Controlla che backend sia online

**Database vuoto?**
- Esegui `python init_db.py` dalla Shell di Render

---

## ⏱️ TEMPO TOTALE STIMATO: 15-20 minuti

**Poi l'app è ONLINE e FUNZIONANTE!** 🚀📰

