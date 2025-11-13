# Script per creare un task schedulato Windows che avvia NewsFlow all'avvio del PC
# Esegui questo script UNA VOLTA SOLA come Amministratore

Write-Host "🔧 Creazione Task Scheduler per NewsFlow" -ForegroundColor Green
Write-Host ""

# Verifica privilegi amministratore
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "❌ Questo script richiede privilegi di Amministratore!" -ForegroundColor Red
    Write-Host "   Clicca destro su PowerShell e seleziona 'Esegui come amministratore'" -ForegroundColor Yellow
    exit 1
}

$rootDir = $PSScriptRoot
$scriptPath = Join-Path $rootDir "avvia_tutto.ps1"

# Verifica che lo script esista
if (-not (Test-Path $scriptPath)) {
    Write-Host "❌ Script avvia_tutto.ps1 non trovato!" -ForegroundColor Red
    exit 1
}

# Nome del task
$taskName = "NewsFlow_AutoStart"

# Verifica se il task esiste già
$existingTask = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
if ($existingTask) {
    Write-Host "⚠️  Task già esistente. Lo rimuovo..." -ForegroundColor Yellow
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
}

# Crea l'azione (esegue PowerShell con lo script)
$action = New-ScheduledTaskAction -Execute "powershell.exe" `
    -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$scriptPath`"" `
    -WorkingDirectory $rootDir

# Crea il trigger (all'avvio del sistema)
$trigger = New-ScheduledTaskTrigger -AtStartup

# Imposta le impostazioni del task
$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -RunOnlyIfNetworkAvailable:$false `
    -RestartCount 3 `
    -RestartInterval (New-TimeSpan -Minutes 1)

# Crea il principal (esegue come utente corrente)
$principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive

# Registra il task
try {
    Register-ScheduledTask -TaskName $taskName `
        -Action $action `
        -Trigger $trigger `
        -Settings $settings `
        -Principal $principal `
        -Description "Avvia automaticamente NewsFlow backend all'avvio del PC" | Out-Null
    
    Write-Host "✅ Task creato con successo!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📋 Dettagli:" -ForegroundColor Cyan
    Write-Host "   Nome: $taskName" -ForegroundColor White
    Write-Host "   Trigger: All'avvio del sistema" -ForegroundColor White
    Write-Host "   Script: $scriptPath" -ForegroundColor White
    Write-Host ""
    Write-Host "💡 Per gestire il task:" -ForegroundColor Yellow
    Write-Host "   • Apri 'Utilità di pianificazione' (taskschd.msc)" -ForegroundColor Gray
    Write-Host "   • Cerca 'NewsFlow_AutoStart'" -ForegroundColor Gray
    Write-Host ""
    Write-Host "💡 Per rimuovere il task:" -ForegroundColor Yellow
    Write-Host "   Unregister-ScheduledTask -TaskName '$taskName' -Confirm:`$false" -ForegroundColor Gray
    
} catch {
    Write-Host "❌ Errore durante la creazione del task:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    exit 1
}

