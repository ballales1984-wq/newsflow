# ✈️ Deploy Backend su Fly.io (GRATUITO - Nessuna carta di credito!)

## ✅ Vantaggi Fly.io
- **100% GRATUITO**: Nessuna carta di credito richiesta
- **Nessun sleep mode**: Backend sempre online
- **3 VM gratuite**: Condivise ma sempre attive
- **160GB traffico/mese**: Molto generoso
- **HTTPS incluso**: Certificato SSL automatico
- **Deploy globale**: Edge computing

## 📋 Setup Fly.io (10 minuti)

### 1. Installa Fly CLI
**Windows (PowerShell):**
```powershell
iwr https://fly.io/install.ps1 -useb | iex
```

**Oppure scarica da:** https://fly.io/docs/getting-started/installing-flyctl/

### 2. Crea Account
```bash
flyctl auth signup
```
- Apri browser e registrati (email + password)
- **Nessuna carta di credito richiesta!** ✅

### 3. Login
```bash
flyctl auth login
```

### 4. Crea Dockerfile (se non esiste)
Crea `backend/Dockerfile`:
```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Copia requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia tutto il backend
COPY . .

# Esponi porta (Fly usa 8080 di default)
EXPOSE 8080

# Avvia FastAPI
CMD ["python", "-m", "uvicorn", "app.main_simple:app", "--host", "0.0.0.0", "--port", "8080"]
```

### 5. Crea fly.toml
Nella directory `backend/`, esegui:
```bash
cd backend
flyctl launch
```

Rispondi alle domande:
- **App name**: `newsflow-backend` (o quello che preferisci)
- **Region**: Scegli più vicino (es: `fra` per Frankfurt)
- **Postgres**: No (non necessario)
- **Redis**: No (non necessario)

### 6. Deploy!
```bash
flyctl deploy
```

### 7. Ottieni URL
```bash
flyctl status
```
Oppure nel dashboard: https://fly.io/dashboard

URL sarà tipo: `https://newsflow-backend.fly.dev`

### 8. Configura CORS
Crea file `backend/fly.toml` e aggiungi:
```toml
[env]
  CORS_ORIGINS = "https://newsflow-orcin.vercel.app,http://localhost:4200"
```

Rideploy:
```bash
flyctl deploy
```

## 📝 Aggiorna Frontend
Dopo il deploy, aggiorna `frontend/src/environments/environment.prod.ts`:
```typescript
apiUrl: 'https://newsflow-backend.fly.dev/api/v1'
```

## 🔄 Deploy Automatico
Per deploy automatico da GitHub, usa GitHub Actions (vedi sotto).

## 💰 Costi
- **Gratuito**: 3 VM condivise + 160GB traffico/mese
- **Nessuna carta di credito**: Richiesta solo per upgrade
- **Monitoraggio**: Dashboard mostra uso gratuito

## ⚠️ Note Importanti
- **Nessun sleep mode**: Backend sempre online! ✅
- **VM condivise**: Performance buone per la maggior parte dei casi
- **HTTPS**: Incluso automaticamente
- **Logs**: `flyctl logs` o dashboard

## 🎯 Risultato
✅ Backend sempre online (nessun sleep mode!)
✅ 100% GRATUITO (nessuna carta di credito!)
✅ HTTPS incluso
✅ Deploy globale
✅ Puoi spegnere il PC!

## 🚀 Comandi Utili
```bash
# Deploy
flyctl deploy

# Logs in tempo reale
flyctl logs

# Status
flyctl status

# Open dashboard
flyctl dashboard

# SSH al container
flyctl ssh console
```

## 🔄 GitHub Actions (Deploy Automatico)
Crea `.github/workflows/fly-deploy.yml`:
```yaml
name: Deploy to Fly.io

on:
  push:
    branches: [main]
    paths:
      - 'backend/**'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: superfly/flyctl-actions/setup-flyctl@master
      - run: flyctl deploy --remote-only
        working-directory: ./backend
        env:
          FLY_API_TOKEN: ${{ secrets.FLY_API_TOKEN }}
```

Ottieni token: `flyctl auth token` → Aggiungi a GitHub Secrets come `FLY_API_TOKEN`

## 🆚 Confronto
| Feature | Render | Railway | Fly.io |
|---------|--------|---------|--------|
| Gratuito | ⚠️ 750h/mese | ⚠️ $5 credito | ✅ 100% gratis |
| Carta di credito | ❌ No | ✅ Sì | ❌ No |
| Sleep Mode | ⚠️ Sì (15min) | ✅ No | ✅ No |
| Setup | Facile | Facilissimo | Medio |

## 🎉 Vantaggi Fly.io
✅ **VERAMENTE GRATUITO** (nessuna carta!)
✅ Nessun sleep mode
✅ 160GB traffico/mese
✅ Deploy globale (edge computing)
✅ Più affidabile di Render

