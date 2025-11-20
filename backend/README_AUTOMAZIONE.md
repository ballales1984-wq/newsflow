# 🤖 Automatizzazione Aggiornamento Notizie

Script per automatizzare l'aggiornamento quotidiano delle notizie NewsFlow.

## 📋 Script Disponibili

### 1. `AGGIORNA_NOTIZIE_AUTOMATICO.ps1`
Script principale che esegue l'intero processo di aggiornamento:
- ✅ Raccolta notizie dai feed RSS
- ✅ Aggiornamento file JSON (backend e frontend)
- ✅ Commit e push su GitHub
- ✅ Aggiornamento repository su PythonAnywhere

**Uso:**
```powershell
# Esecuzione normale
.\AGGIORNA_NOTIZIE_AUTOMATICO.ps1

# Salta push su GitHub
.\AGGIORNA_NOTIZIE_AUTOMATICO.ps1 -SkipPush

# Salta aggiornamento PythonAnywhere
.\AGGIORNA_NOTIZIE_AUTOMATICO.ps1 -SkipPythonAnywhere
```

### 2. `CREA_TASK_SCHEDULER.ps1`
Crea un Task Scheduler Windows per eseguire l'aggiornamento automaticamente ogni giorno.

**Uso:**
```powershell
# Esegui come Amministratore
.\CREA_TASK_SCHEDULER.ps1
```

**Configurazione default:**
- ⏰ Esecuzione: Ogni giorno alle 06:00
- 🔄 Modalità: Automatico
- 🌐 Richiede connessione internet

**Per modificare l'orario:**
1. Apri Task Scheduler (`taskschd.msc`)
2. Cerca: `NewsFlow-AggiornamentoNotizie`
3. Clicca destro → Proprietà → Trigger
4. Modifica l'orario

### 3. `AGGIORNA_NOTIZIE_AUTOMATICO.bat`
Versione batch alternativa (per compatibilità).

**Uso:**
```cmd
AGGIORNA_NOTIZIE_AUTOMATICO.bat
```

## 🚀 Setup Rapido

### Opzione 1: Task Scheduler (Consigliato)
```powershell
# 1. Apri PowerShell come Amministratore
# 2. Vai nella cartella backend
cd C:\Users\user\news\backend

# 3. Esegui lo script di creazione task
.\CREA_TASK_SCHEDULER.ps1

# 4. Verifica che il task sia stato creato
#    Task Scheduler → Cerca "NewsFlow-AggiornamentoNotizie"
```

### Opzione 2: Esecuzione Manuale
```powershell
# Esegui quando vuoi aggiornare le notizie
.\AGGIORNA_NOTIZIE_AUTOMATICO.ps1
```

## 📊 Cosa Fa lo Script

1. **Raccolta Notizie**
   - Esegue `collect_italian_priority.py`
   - Raccoglie notizie da tutti i feed RSS configurati
   - Estrae immagini quando disponibili

2. **Aggiornamento File**
   - Copia `italian_priority_news.json` → `final_news_italian.json`
   - Aggiorna anche il file frontend

3. **Git Commit & Push**
   - Aggiunge i file modificati
   - Crea commit con timestamp
   - Push su GitHub

4. **Aggiornamento PythonAnywhere**
   - Invia comando `git pull` via API
   - Aggiorna il repository sul server

## 🔧 Configurazione

### Token PythonAnywhere
Il token è già configurato nello script. Se necessario, modifica:
```powershell
$TOKEN = 'f17e14d4b1a12e0bf325cc0c1d8f9871fe50e599'
```

### Orario Esecuzione
Modifica in `CREA_TASK_SCHEDULER.ps1`:
```powershell
$trigger = New-ScheduledTaskTrigger -Daily -At 6:00AM  # Cambia l'orario qui
```

## 🧪 Test

### Test Manuale
```powershell
# Esegui lo script manualmente
.\AGGIORNA_NOTIZIE_AUTOMATICO.ps1
```

### Test Task Scheduler
1. Apri Task Scheduler
2. Cerca `NewsFlow-AggiornamentoNotizie`
3. Clicca destro → **Esegui**
4. Controlla i log

## 📝 Log e Monitoraggio

Lo script mostra output dettagliato durante l'esecuzione:
- ✅ Operazioni completate
- ⚠️ Avvisi
- ❌ Errori

Per vedere i log del Task Scheduler:
1. Task Scheduler → `NewsFlow-AggiornamentoNotizie`
2. Tab "Storia" → Visualizza eventi

## 🔍 Troubleshooting

### Errore: "Git non configurato"
```powershell
git config --global user.name "Tuo Nome"
git config --global user.email "tua@email.com"
```

### Errore: "Python non trovato"
Verifica che Python sia nel PATH:
```powershell
python --version
```

### Task non si esegue
1. Verifica che il PC sia acceso all'orario programmato
2. Verifica connessione internet
3. Controlla i log in Task Scheduler

### Errore PythonAnywhere
Lo script continua anche se PythonAnywhere fallisce. Puoi aggiornare manualmente:
```bash
cd ~/newsflow && git pull
```

## 💡 Suggerimenti

- **Orario consigliato**: 06:00 (prima che gli utenti accedano)
- **Frequenza**: Una volta al giorno è sufficiente
- **Backup**: Git mantiene storico di tutte le versioni
- **Monitoraggio**: Controlla periodicamente che il task funzioni

## 📞 Supporto

Se hai problemi:
1. Controlla i log dello script
2. Verifica che Git sia configurato
3. Verifica connessione internet
4. Controlla Task Scheduler per errori

---

**✅ Con questo setup, le notizie si aggiorneranno automaticamente ogni giorno!**

