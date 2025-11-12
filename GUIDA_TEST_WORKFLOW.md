# 🚀 GUIDA PASSO-PASSO: TEST WORKFLOW GITHUB ACTIONS

## 📋 ISTRUZIONI DETTAGLIATE

### PASSO 1: Apri GitHub Actions
1. Vai su: https://github.com/ballales1984-wq/newsflow/actions
2. Se non sei loggato, fai login con il tuo account GitHub

### PASSO 2: Trova il Workflow
1. Nella lista dei workflow, cerca **"Update News Automatically"**
2. Clicca sul nome del workflow

### PASSO 3: Esegui Manualmente
1. Clicca sul pulsante blu **"Run workflow"** (in alto a destra)
2. Assicurati che il branch sia **"main"**
3. Clicca di nuovo **"Run workflow"** (pulsante verde)

### PASSO 4: Monitora l'Esecuzione
1. Vedrai una nuova esecuzione nella lista (con un punto giallo/arancione)
2. Clicca sull'esecuzione per vedere i dettagli
3. Vedrai gli step in esecuzione:
   - ✅ Checkout repository
   - ✅ Setup Python
   - ✅ Install dependencies
   - ✅ Collect Italian Priority News
   - ✅ Update final_news_italian.json
   - ✅ Commit and push changes

### PASSO 5: Attendi Completamento
- ⏳ Tempo stimato: **5-7 minuti**
- 🟡 Giallo = In esecuzione
- 🟢 Verde = Completato con successo
- 🔴 Rosso = Errore (raro)

### PASSO 6: Verifica Risultati
Dopo il completamento:
1. Controlla che tutti gli step siano verdi ✅
2. Vai su: https://github.com/ballales1984-wq/newsflow/commits
3. Dovresti vedere un nuovo commit: "🤖 Auto-update: Aggiornate notizie..."
4. Render farà automaticamente redeploy (3-5 minuti)
5. Vercel farà automaticamente redeploy (2-3 minuti)

## 🎯 COSA SUCCEDE DURANTE IL TEST

1. **GitHub Actions** esegue gli script Python
2. Raccoglie nuove notizie da RSS feeds
3. Aggiorna `final_news_italian.json`
4. Fa commit e push automatico
5. **Render** rileva il push → Redeploy backend
6. **Vercel** rileva il push → Redeploy frontend
7. L'app mostra le nuove notizie!

## ✅ RISULTATO ATTESO

- ✅ Workflow completato con successo
- ✅ Nuovo commit su GitHub
- ✅ Render fa redeploy automatico
- ✅ Vercel fa redeploy automatico
- ✅ App aggiornata con nuove notizie

## 🆘 SE QUALCOSA VA STORTO

- **Workflow fallisce**: Controlla i log per vedere quale step ha fallito
- **Render non fa redeploy**: Verifica che Render sia collegato al repo GitHub
- **Vercel non fa redeploy**: Verifica che Vercel sia collegato al repo GitHub

## 💡 DOPO IL TEST

Se tutto funziona:
- ✅ Il workflow si eseguirà automaticamente ogni 6 ore
- ✅ Non devi fare più nulla manualmente
- ✅ L'app si aggiornerà da sola per sempre!

