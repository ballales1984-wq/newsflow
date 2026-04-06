# Script per creare automazione Task Scheduler - Versione Corretta
# Esegue AGGIORNA_NOTIZIE_NUOVO.ps1 ogni 24 ore alle 06:00

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "="*60 -ForegroundColor Cyan
Write-Host "CREAZIONE AUTOMAZIONE 24H" -ForegroundColor Yellow
Write-Host "="*60 -ForegroundColor Cyan
Write-Host ""

# Verifica privilegi amministratore
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "[ERRORE] Questo script richiede privilegi di Amministratore!" -ForegroundColor Red
    Write-Host "   Esegui: Start-Process powershell -Verb RunAs -ArgumentList '-File ""$PSCommandPath""'" -ForegroundColor Yellow
    exit 1
}

# Configurazione
$scriptPath = "c:/Users/user/news/AGGIORNA_NOTIZIE_NUOVO.ps1"
$taskName = "NewsFlow-Aggiornamento24H"
$description = "Aggiornamento automatico notizie NewsFlow ogni 24 ore"

Write-Host "[INFO] Configurazione:" -ForegroundColor Cyan
Write-Host "       Nome Task: $taskName" -ForegroundColor White
Write-Host "       Script: $scriptPath" -ForegroundColor White
Write-Host "       Orario: 06:00 ogni giorno" -ForegroundColor White
Write-Host ""

# Verifica che lo script esista
if (-not (Test-Path $scriptPath)) {
    Write-Host "[ERRORE] Script non trovato: $scriptPath" -ForegroundColor Red
    exit 1
}

# Rimuovi task esistente se presente
try {
    $existingTask = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
    if ($existingTask) {
        Write-Host "[INFO] Rimuovo task esistente..." -ForegroundColor Yellow
        Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
    }
} catch {
    Write-Host "[INFO] Nessun task esistente" -ForegroundColor Gray
}

# Crea azione
$action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$scriptPath`""

# Crea trigger (ogni giorno alle 06:00)
$trigger = New-ScheduledTaskTrigger -Daily -At 6:00AM

# Impostazioni
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -WakeToRun -RestartCount 3 -RestartInterval (New-TimeSpan -Minutes 5)

# Principal
$principal = New-ScheduledTaskPrincipal -UserId "$env:USERDOMAIN\$env:USERNAME" -LogonType Interactive

# Registra task
try {
    Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -Principal $principal -Description $description -Force

    Write-Host ""
    Write-Host "[OK] Task Scheduler creato!" -ForegroundColor Green
    Write-Host ""
    Write-Host "[INFO] Dettagli:" -ForegroundColor Cyan
    Write-Host "       - Nome: $taskName" -ForegroundColor White
    Write-Host "       - Orario: 06:00 ogni giorno" -ForegroundColor White
    Write-Host "       - Script: $scriptPath" -ForegroundColor White
    Write-Host ""
    Write-Host "[TEST] Per testare ora:" -ForegroundColor Yellow
    Write-Host "       Get-ScheduledTask -TaskName '$taskName' | Start-ScheduledTask" -ForegroundColor Gray
    Write-Host ""
    Write-Host "[MODIFICA] Per modificare l'orario:" -ForegroundColor Yellow
    Write-Host "       1. Apri: taskschd.msc" -ForegroundColor Gray
    Write-Host "       2. Trova: $taskName" -ForegroundColor Gray
    Write-Host "       3. Proprieta -> Trigger" -ForegroundColor Gray
    Write-Host ""

} catch {
    Write-Host "[ERRORE] $_.Exception.Message" -ForegroundColor Red
    exit 1
}

