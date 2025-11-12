# 🔔 Come Risvegliare l'App

## Problema
Render (backend) va in **sleep mode** dopo 15 minuti di inattività. Quando l'app viene aperta dopo questo periodo, ci vuole tempo per "svegliare" il backend.

## Soluzioni Implementate

### ✅ 1. GitHub Actions - Keep-Alive Automatico
**File:** `.github/workflows/keep-alive.yml`

- **Cosa fa:** Fa ping automatico al backend ogni **15 minuti**
- **Quando:** 24/7, anche quando nessuno usa l'app
- **Stato:** ✅ Attivo dopo il prossimo push

### ✅ 2. Frontend Keep-Alive Service
**File:** `frontend/src/app/services/keep-alive.service.ts`

- **Cosa fa:** Quando l'app è aperta, fa ping ogni **10 minuti**
- **Quando:** Solo quando qualcuno sta usando l'app
- **Stato:** ✅ Attivo dopo il prossimo deploy

### ✅ 3. Timeout Aumentato
**File:** `frontend/src/app/pages/home/home.component.ts`

- **Cosa fa:** Timeout di **60 secondi** per permettere il risveglio
- **Quando:** Ad ogni caricamento delle notizie
- **Stato:** ✅ Già attivo

## Come Funziona Ora

1. **Automatico (GitHub Actions):**
   - Ogni 15 minuti GitHub fa ping → Backend sempre sveglio
   - Non devi fare nulla!

2. **Quando l'utente apre l'app:**
   - Se il backend è in sleep, l'app aspetta fino a 60 secondi
   - Il servizio keep-alive mantiene il backend sveglio mentre l'app è aperta

## Test Manuale

Se vuoi testare manualmente il risveglio:

```bash
# Ping diretto al backend
curl https://newsflow-backend-v2.onrender.com/api/health
```

Oppure apri nel browser:
```
https://newsflow-backend-v2.onrender.com/api/health
```

## Verifica Stato

1. **GitHub Actions:**
   - Vai su: https://github.com/[tuo-username]/news/actions
   - Cerca workflow "Keep Backend Alive"
   - Verifica che sia attivo e funzionante

2. **Console Browser:**
   - Apri l'app web
   - Apri DevTools (F12)
   - Nella console vedrai: `🔄 Servizio Keep-Alive avviato`
   - Ogni 10 minuti vedrai: `✅ Backend sveglio`

## Note

- Il backend Render FREE ha un limite di **750 ore/mese**
- Con il keep-alive ogni 15 minuti = ~720 ore/mese ✅
- Se superi il limite, Render si ferma (ma è raro)

## Prossimi Passi

1. ✅ Push delle modifiche
2. ✅ Deploy automatico su Vercel (frontend)
3. ✅ GitHub Actions si attiva automaticamente
4. ✅ L'app sarà sempre sveglia! 🎉

