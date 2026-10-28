# 🤖 Automazione Aggiornamento Notizie - Ogni 24 Ore

## 📋 Script Disponibili

### 1. `AGGIORNA_TUTTO.ps1`
Script completo che esegue tutto in un'unica operazione:
- ✅ Raccolta notizie da feed RSS
- ✅ Sincronizzazione file JSON in tutte le cartelle
- ✅ Generazione digest giornaliero
- ✅ Commit e push su GitHub
- ✅ Deploy automatico su Vercel

**Uso:**
```powershell
.\AGGIORNA_TUTTO.ps1
```

### 2. `CREA_AUTOMAZIONE_24H.ps1`
Crea un Task Scheduler Windows per eseguire l'aggiornamento automaticamente ogni 24 ore.

**Uso:**
```powershell
# Esegui come Amministratore
.\CREA_AUTOMAZIONE_24H.ps1
```

**Oppure:**
```powershell
Start-Process powershell -Verb RunAs -ArgumentList '-File ".\CREA_AUTOMAZIONE_24H.ps1"'
```

## 🚀 Setup Rapido

### Passo 1: Crea l'automazione (una volta sola)
```powershell
# Apri PowerShell come Amministratore
# Poi esegui:
.\CREA_AUTOMAZIONE_24H.ps1
```

### Passo 2: Verifica
```powershell
# Controlla che il task sia stato creato
Get-ScheduledTask -TaskName "NewsFlow-Aggiornamento24H"
```

### Passo 3: Test (opzionale)
```powershell
# Esegui manualmente per testare
.\AGGIORNA_TUTTO.ps1
```

## ⚙️ Configurazione

**Orario predefinito:** Ogni giorno alle 06:00

**Per modificare:**
1. Apri Task Scheduler (`taskschd.msc`)
2. Cerca: `NewsFlow-Aggiornamento24H`
3. Clicca destro → Proprietà → Trigger
4. Modifica l'orario o la frequenza

## 📊 Cosa Fa l'Automazione

Ogni 24 ore (alle 06:00):
1. Raccoglie notizie da feed RSS italiani e internazionali
2. Genera il digest giornaliero
3. Sincronizza i file JSON in tutte le cartelle
4. Fa commit e push su GitHub
5. Vercel fa deploy automatico (2-3 minuti)

## 🧪 Test Manuale

Per testare senza aspettare:
```powershell
.\AGGIORNA_TUTTO.ps1
```

Oppure dal Task Scheduler:
- Task Scheduler → Cerca "NewsFlow-Aggiornamento24H"
- Clicca destro → Esegui

## 🗑️ Rimozione Automazione

Se vuoi rimuovere l'automazione:
```powershell
Unregister-ScheduledTask -TaskName "NewsFlow-Aggiornamento24H" -Confirm:$false
```

## 📝 Note

- Il task richiede connessione internet
- Il task si esegue anche se il PC è in batteria
- Se il PC è spento, il task si esegue al prossimo avvio (se configurato)
- I log sono visibili in Task Scheduler → Cronologia

## 🔍 Verifica Stato

```powershell
# Vedi dettagli del task
Get-ScheduledTask -TaskName "NewsFlow-Aggiornamento24H" | Format-List

# Vedi prossima esecuzione
Get-ScheduledTask -TaskName "NewsFlow-Aggiornamento24H" | Get-ScheduledTaskInfo
```

