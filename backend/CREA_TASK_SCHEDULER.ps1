# Script per creare un Task Scheduler che esegue l'aggiornamento automatico ogni giorno
# Richiede esecuzione come Amministratore

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "="*70 -ForegroundColor Cyan
Write-Host "📅 CREAZIONE TASK SCHEDULER - AGGIORNAMENTO NOTIZIE" -ForegroundColor Yellow
Write-Host "="*70 -ForegroundColor Cyan
Write-Host ""

# Verifica privilegi amministratore
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "⚠️  Questo script richiede privilegi di Amministratore!" -ForegroundColor Red
    Write-Host "   Esegui PowerShell come Amministratore e riprova" -ForegroundColor Yellow
    Write-Host ""
    exit 1
}

# Percorsi
$scriptPath = Join-Path $PSScriptRoot "AGGIORNA_NOTIZIE_AUTOMATICO.ps1"
$taskName = "NewsFlow-AggiornamentoNotizie"
$description = "Aggiornamento automatico quotidiano delle notizie NewsFlow"

Write-Host "📋 Configurazione Task:" -ForegroundColor Cyan
Write-Host "   Nome: $taskName" -ForegroundColor White
Write-Host "   Script: $scriptPath" -ForegroundColor White
Write-Host "   Esecuzione: Ogni giorno alle 06:00" -ForegroundColor White
Write-Host ""

# Verifica che lo script esista
if (-not (Test-Path $scriptPath)) {
    Write-Host "❌ Script non trovato: $scriptPath" -ForegroundColor Red
    exit 1
}

# Rimuovi task esistente se presente
try {
    $existingTask = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
    if ($existingTask) {
        Write-Host "🗑️  Rimozione task esistente..." -ForegroundColor Yellow
        Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
        Write-Host "   ✅ Task rimosso" -ForegroundColor Green
    }
} catch {
    Write-Host "   ℹ️  Nessun task esistente da rimuovere" -ForegroundColor Gray
}

# Crea action (comando da eseguire)
$action = New-ScheduledTaskAction `
    -Execute "powershell.exe" `
    -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$scriptPath`""

# Crea trigger (ogni giorno alle 06:00)
$trigger = New-ScheduledTaskTrigger -Daily -At 6:00AM

# Impostazioni task
$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -RunOnlyIfNetworkAvailable `
    -WakeToRun

# Crea principal (esegui come utente corrente)
$principal = New-ScheduledTaskPrincipal -UserId "$env:USERDOMAIN\$env:USERNAME" -LogonType Interactive

# Registra il task
try {
    Register-ScheduledTask `
        -TaskName $taskName `
        -Action $action `
        -Trigger $trigger `
        -Settings $settings `
        -Principal $principal `
        -Description $description `
        -Force
    
    Write-Host ""
    Write-Host "✅ Task Scheduler creato con successo!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📋 Dettagli:" -ForegroundColor Cyan
    Write-Host "   • Nome: $taskName" -ForegroundColor White
    Write-Host "   • Esecuzione: Ogni giorno alle 06:00" -ForegroundColor White
    Write-Host "   • Script: $scriptPath" -ForegroundColor White
    Write-Host ""
    Write-Host "💡 Per modificare:" -ForegroundColor Yellow
    Write-Host "   • Apri Task Scheduler (taskschd.msc)" -ForegroundColor Gray
    Write-Host "   • Cerca: $taskName" -ForegroundColor Gray
    Write-Host "   • Modifica trigger, orario, ecc." -ForegroundColor Gray
    Write-Host ""
    Write-Host "🧪 Per testare:" -ForegroundColor Yellow
    Write-Host "   • Task Scheduler → Clicca destro sul task → Esegui" -ForegroundColor Gray
    Write-Host "   • Oppure: .\AGGIORNA_NOTIZIE_AUTOMATICO.ps1" -ForegroundColor Gray
    Write-Host ""
    
} catch {
    Write-Host ""
    Write-Host "❌ Errore durante la creazione del task: $_" -ForegroundColor Red
    Write-Host ""
    exit 1
}

