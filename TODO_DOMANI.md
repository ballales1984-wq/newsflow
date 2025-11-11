# 📋 TODO DOMANI - Sistemare Versione Web

**Data:** 12 Novembre 2024

---

## 🌐 VERCEL - Sistemare 404

### Problema:
Frontend dà 404 invece di caricare l'app

### Soluzioni da provare:

#### Opzione 1: Configurazione Settings
1. Vercel Dashboard → `newsflow` → Settings
2. Build & Development Settings:
   ```
   Framework: Angular (o Other)
   Root Directory: frontend
   Build Command: npm run build
   Output Directory: dist/newsflow/browser
   ```
3. Save → Redeploy

#### Opzione 2: Ricrea progetto
1. Delete project
2. New Project → Import `newsflow`
3. Configura manualmente con settings sopra

#### Opzione 3: Verifica file output
1. Controlla dove Angular genera i file
2. Potrebbe essere:
   - `dist/newsflow`
   - `dist/newsflow/browser`  
   - `frontend/dist/newsflow/browser`

---

## 🔄 RENDER - Verifica Notizie

### Da fare:
1. Aspetta ultimo deploy finisca (8da66ba)
2. Testa: https://newsflow-backend-mzw7.onrender.com/api/v1/articles
3. Verifica mostra le 12 notizie embedded
4. Se SÌ → Perfetto!
5. Se NO → Debug necessario

---

## 🧪 TEST COMPLETO ONLINE

Quando Vercel funziona:

### Frontend Online:
- [ ] Homepage carica
- [ ] 12 notizie visualizzate
- [ ] Pulsante "Leggi" funziona
- [ ] Pulsante "Salva" funziona
- [ ] Pulsante "Condividi" funziona
- [ ] Pagina "Salvati" funziona
- [ ] Categorie filtrano
- [ ] Ricerca funziona

### Backend Online:
- [ ] `/` risponde
- [ ] `/api/health` risponde
- [ ] `/api/v1/articles` → 12 notizie
- [ ] `/api/v1/categories` → 8 categorie
- [ ] CORS funziona per Vercel

---

## 🎯 OBIETTIVO DOMANI:

✅ App online completamente funzionante  
✅ Accessibile da https://newsflow-orcin.vercel.app  
✅ Tutte le features operative  

**Tempo stimato: 15-30 minuti**

---

## 🚀 DOPO CHE FUNZIONA:

### Prossimi sviluppi:
- [ ] Personalizzare per SINTESI (logo, colori, testi)
- [ ] Aggiungere più fonti RSS
- [ ] Sistema raccolta automatica
- [ ] Feature "Spiegami questa notizia"
- [ ] Newsletter
- [ ] TG AI

---

*Creato: 11 Nov 2024, 02:00 AM*

