# 🚀 Deploy Backend su Vercel

## Configurazione Completata

Il backend è stato configurato per funzionare su Vercel come serverless functions.

## Struttura

- **`api/[...path].py`** - Serverless function che wrappa FastAPI usando Mangum
- **`vercel.json`** - Configurazione Vercel per frontend e backend
- **`requirements.txt`** - Dipendenze Python per Vercel (include mangum)

## Come Funziona

1. **Frontend**: Build da `frontend/` e deploy come static site
2. **Backend**: API routes `/api/*` gestite da serverless functions Python
3. **Stesso dominio**: Frontend e backend sono sullo stesso dominio Vercel

## URL

- **Frontend**: `https://newsflow-orcin.vercel.app/`
- **Backend API**: `https://newsflow-orcin.vercel.app/api/v1/*`

## Deploy

Il deploy su Vercel è automatico quando fai push su GitHub:

```bash
git add .
git commit -m "Migrate backend to Vercel"
git push origin main
```

Vercel rileverà automaticamente:
- Frontend Angular da `frontend/`
- Backend Python da `api/`

## Note Importanti

1. **File JSON**: I file `final_news_italian.json` e `all_sources_news.json` devono essere nella directory `backend/` e saranno inclusi nel deploy
2. **CORS**: Configurato per permettere richieste dal frontend Vercel
3. **Environment Variables**: Configurate in `vercel.json` (CORS_ORIGINS)

## Vantaggi Vercel vs Render

✅ Nessun limite di pipeline minutes  
✅ Deploy automatico su ogni push  
✅ Stesso dominio per frontend e backend  
✅ Serverless functions (scalabile automaticamente)  
✅ CDN globale per performance ottimali

## Troubleshooting

Se le API non funzionano:
1. Verifica che `mangum` sia in `requirements.txt`
2. Controlla i log su Vercel Dashboard → Functions
3. Verifica che i file JSON siano nella directory `backend/`

