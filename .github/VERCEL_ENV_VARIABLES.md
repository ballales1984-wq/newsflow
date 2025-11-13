# Variabili d'Ambiente Vercel

## Configurazione Necessaria

Vai su **Vercel Dashboard** → **Settings** → **Environment Variables**

### Variabili da Configurare:

1. **CORS_ORIGINS** (NECESSARIA)
   - **Valore**: `https://newsflow-orcin.vercel.app,https://newsflow-three.vercel.app`
   - **Ambiente**: ✅ Production, ✅ Preview, ✅ Development

2. **SECRET_KEY** (Opzionale, per JWT/auth)
   - **Valore**: Qualsiasi stringa segreta (es: `your-secret-key-here`)
   - **Ambiente**: ✅ Production, ✅ Preview, ✅ Development

## Verifica Configurazione

Dopo aver configurato le variabili:

1. **Redeploy** il progetto su Vercel (Settings → Redeploy)
2. **Testa l'endpoint debug**: `https://newsflow-orcin.vercel.app/api/debug/files`
3. **Verifica che i file JSON siano accessibili**

## Problema Noto

Se le notizie non compaiono, potrebbe essere che:
- I file JSON non sono accessibili dalle serverless functions
- Il path dei file JSON non è corretto su Vercel
- Le variabili d'ambiente non sono state applicate correttamente

**Soluzione**: Testa l'endpoint `/api/debug/files` per vedere se i file sono accessibili.

