# 🚀 NewsFlow - Script di Avvio Automatico

Questo documento spiega come configurare l'avvio automatico di NewsFlow all'avvio del PC.

## 📋 Script Disponibili

### 1. `avvia_backend.ps1`
Avvia il backend locale su `http://localhost:8000`

**Uso:**
```powershell
.\avvia_backend.ps1
```

**Cosa fa:**
- Ferma eventuali processi esistenti sulla porta 8000
- Avvia il server backend con uvicorn
- Verifica che il backend sia attivo

---

### 2. `sincronizza_e_deploy.ps1`
Sincronizza i file JSON e fa deploy su Vercel

**Uso:**
```powershell
.\sincronizza_e_deploy.ps1
```

**Cosa fa:**
- Copia `final_news_italian.json` da root a `api/` e `backend/`
- Fa commit e push su GitHub
- Vercel avvia automaticamente il deploy

---

### 3. `avvia_tutto.ps1`
Script principale che avvia tutto il sistema

**Uso:**
```powershell
.\avvia_tutto.ps1
```

**Cosa fa:**
- Avvia il backend locale
- Chiede se fare deploy su Vercel (opzionale)

---

### 4. `crea_task_scheduler.ps1`
Crea un task Windows che avvia NewsFlow all'avvio del PC

**Uso (come Amministratore):**
```powershell
# Apri PowerShell come Amministratore
.\crea_task_scheduler.ps1
```

**Cosa fa:**
- Crea un task schedulato Windows
- Il task esegue `avvia_tutto.ps1` all'avvio del sistema
- Funziona solo se eseguito come Amministratore

---

## 🔧 Configurazione Avvio Automatico

### Metodo 1: Task Scheduler (Consigliato)

1. **Apri PowerShell come Amministratore:**
   - Cerca "PowerShell" nel menu Start
   - Clicca destro → "Esegui come amministratore"

2. **Vai alla directory del progetto:**
   ```powershell
   cd C:\Users\user\news
   ```

3. **Esegui lo script di configurazione:**
   ```powershell
   .\crea_task_scheduler.ps1
   ```

4. **Verifica il task:**
   - Apri "Utilità di pianificazione" (taskschd.msc)
   - Cerca "NewsFlow_AutoStart"
   - Verifica che sia abilitato

### Metodo 2: Cartella Avvio Windows

1. **Apri la cartella Avvio:**
   - Premi `Win + R`
   - Digita: `shell:startup`
   - Premi Invio

2. **Crea un collegamento:**
   - Clicca destro → Nuovo → Collegamento
   - Percorso: `powershell.exe -NoProfile -ExecutionPolicy Bypass -File "C:\Users\user\news\avvia_tutto.ps1"`
   - Nome: "NewsFlow"

---

## 🔍 Verifica Funzionamento

### Backend Locale
Apri il browser e vai su:
- **API**: http://localhost:8000/api/v1/articles?page=1&size=5
- **Docs**: http://localhost:8000/docs

### Deploy Vercel
Controlla lo stato su:
- **Dashboard**: https://vercel.com/dashboard
- **Logs**: Controlla i log di deploy per eventuali errori

---

## 🛠️ Risoluzione Problemi

### Backend non si avvia
1. Verifica che Python sia installato: `python --version`
2. Verifica che le dipendenze siano installate: `pip install -r backend/requirements.txt`
3. Controlla che la porta 8000 sia libera

### Deploy Vercel non funziona
1. Verifica che i file JSON siano sincronizzati:
   ```powershell
   python backend/verifica_articoli_web.py
   ```
2. Verifica che Git sia configurato correttamente
3. Controlla i log di Vercel per errori

### Task Scheduler non funziona
1. Verifica che il task sia abilitato in "Utilità di pianificazione"
2. Controlla i log del task per errori
3. Verifica che PowerShell possa eseguire script (ExecutionPolicy)

---

## 📝 Note Importanti

- **Backend Locale**: Deve essere avviato manualmente o tramite script
- **Vercel**: Si aggiorna automaticamente ad ogni push su GitHub
- **File JSON**: Devono essere sincronizzati manualmente prima del deploy
- **Porta 8000**: Assicurati che sia libera prima di avviare il backend

---

## 🔄 Workflow Consigliato

1. **All'avvio del PC:**
   - Il task schedulato avvia automaticamente il backend

2. **Dopo aver raccolto nuove notizie:**
   ```powershell
   .\sincronizza_e_deploy.ps1
   ```

3. **Per riavviare il backend:**
   ```powershell
   .\avvia_backend.ps1
   ```

---

## ❓ Domande Frequenti

**Q: Il backend si avvia automaticamente?**
A: Sì, se hai configurato il Task Scheduler.

**Q: Come faccio a fermare il backend?**
A: Chiudi la finestra PowerShell o premi Ctrl+C.

**Q: Devo fare deploy manuale ogni volta?**
A: Solo quando hai nuove notizie da pubblicare. Usa `sincronizza_e_deploy.ps1`.

**Q: Perché Vercel non si aggiorna?**
A: Verifica che i file JSON siano sincronizzati e che il push su GitHub sia completato.

