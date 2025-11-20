# Script per creare Task Scheduler che esegue AGGIORNA_TUTTO.ps1 ogni 24 ore
# Richiede esecuzione come Amministratore

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "="*70 -ForegroundColor Cyan
Write-Host "🤖 CREAZIONE AUTOMAZIONE AGGIORNAMENTO 24H" -ForegroundColor Yellow
Write-Host "="*70 -ForegroundColor Cyan
Write-Host ""

# Verifica privilegi amministratore
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "❌ Questo script richiede privilegi di Amministratore!" -ForegroundColor Red
    Write-Host "   Clicca destro su PowerShell e seleziona 'Esegui come amministratore'" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "💡 Oppure esegui manualmente:" -ForegroundColor Cyan
    Write-Host "   Start-Process powershell -Verb RunAs -ArgumentList '-File `"$PSCommandPath`"'" -ForegroundColor Gray
    exit 1
}

# Percorsi
$rootDir = $PSScriptRoot
if (-not $rootDir) {
    $rootDir = Get-Location
}

$scriptPath = Join-Path $rootDir "AGGIORNA_TUTTO.ps1"
$taskName = "NewsFlow-Aggiornamento24H"
$description = "Aggiornamento automatico notizie NewsFlow ogni 24 ore"

Write-Host "📋 Configurazione:" -ForegroundColor Cyan
Write-Host "   Nome Task: $taskName" -ForegroundColor White
Write-Host "   Script: $scriptPath" -ForegroundColor White
Write-Host "   Frequenza: Ogni 24 ore (ogni giorno)" -ForegroundColor White
Write-Host "   Orario: 06:00 (modificabile dopo)" -ForegroundColor White
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
    Write-Host "   ℹ️  Nessun task esistente" -ForegroundColor Gray
}

# Crea action (comando da eseguire)
$action = New-ScheduledTaskAction `
    -Execute "powershell.exe" `
    -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$scriptPath`"" `
    -WorkingDirectory $rootDir

# Crea trigger (ogni giorno alle 06:00)
# Per ogni 24 ore, usiamo Daily trigger
$trigger = New-ScheduledTaskTrigger -Daily -At 6:00AM

# Impostazioni task
$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -RunOnlyIfNetworkAvailable `
    -WakeToRun `
    -RestartCount 3 `
    -RestartInterval (New-TimeSpan -Minutes 5)

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
    Write-Host "   • Frequenza: 24 ore" -ForegroundColor White
    Write-Host ""
    Write-Host "💡 Per modificare orario/frequenza:" -ForegroundColor Yellow
    Write-Host "   1. Apri Task Scheduler (taskschd.msc)" -ForegroundColor Gray
    Write-Host "   2. Cerca: $taskName" -ForegroundColor Gray
    Write-Host "   3. Clicca destro → Proprietà → Trigger" -ForegroundColor Gray
    Write-Host "   4. Modifica orario o frequenza" -ForegroundColor Gray
    Write-Host ""
    Write-Host "🧪 Per testare subito:" -ForegroundColor Yellow
    Write-Host "   • Task Scheduler → Clicca destro sul task → Esegui" -ForegroundColor Gray
    Write-Host "   • Oppure: .\AGGIORNA_TUTTO.ps1" -ForegroundColor Gray
    Write-Host ""
    Write-Host "📊 Per vedere lo stato:" -ForegroundColor Yellow
    Write-Host "   Get-ScheduledTask -TaskName '$taskName' | Format-List" -ForegroundColor Gray
    Write-Host ""
    Write-Host "🗑️  Per rimuovere:" -ForegroundColor Yellow
    Write-Host "   Unregister-ScheduledTask -TaskName '$taskName' -Confirm:`$false" -ForegroundColor Gray
    Write-Host ""
    
} catch {
    Write-Host ""
    Write-Host "❌ Errore durante la creazione del task:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Write-Host ""
    exit 1
}

