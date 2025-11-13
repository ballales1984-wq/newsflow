# Script per avviare backend + frontend + ngrok
# Avvia tutto il necessario per avere NewsFlow pubblico su internet

Write-Host "🚀 Avvio Server Pubblico NewsFlow" -ForegroundColor Cyan
Write-Host ""

# Verifica se ngrok è installato
$ngrokPath = Get-Command ngrok -ErrorAction SilentlyContinue
if (-not $ngrokPath) {
    Write-Host "❌ ngrok non trovato!" -ForegroundColor Red
    Write-Host ""
    Write-Host "📥 INSTALLAZIONE:" -ForegroundColor Yellow
    Write-Host "1. Scarica da: https://ngrok.com/download" -ForegroundColor White
    Write-Host "2. Estrai ngrok.exe in una cartella (es: C:\ngrok\)" -ForegroundColor White
    Write-Host "3. Aggiungi al PATH o metti ngrok.exe nella cartella news" -ForegroundColor White
    Write-Host ""
    Write-Host "OPPURE usa: choco install ngrok (se hai Chocolatey)" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Premi un tasto per chiudere..." -ForegroundColor Gray
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit
}

Write-Host "✅ ngrok trovato!" -ForegroundColor Green
Write-Host ""

# Vai alla directory del progetto
$rootDir = $PSScriptRoot
Set-Location $rootDir

# Avvia backend
Write-Host "🔧 Avvio backend su porta 8000..." -ForegroundColor Yellow
$backendDir = Join-Path $rootDir "backend"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$backendDir'; python -m uvicorn app.main_simple:app --host 0.0.0.0 --port 8000 --reload"
Start-Sleep -Seconds 3

# Verifica che il backend sia attivo
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/api/health" -UseBasicParsing -TimeoutSec 2 -ErrorAction Stop
    Write-Host "✅ Backend attivo!" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Backend in avvio... potrebbe richiedere qualche secondo" -ForegroundColor Yellow
}

# Avvia frontend
Write-Host "🔧 Avvio frontend su porta 4200..." -ForegroundColor Yellow
$frontendDir = Join-Path $rootDir "frontend"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$frontendDir'; npm start"
Start-Sleep -Seconds 5

# Avvia ngrok per backend
Write-Host "🌐 Avvio ngrok per backend (porta 8000)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "ngrok http 8000"
Start-Sleep -Seconds 3

# Avvia ngrok per frontend (opzionale)
Write-Host "🌐 Avvio ngrok per frontend (porta 4200)..." -ForegroundColor Yellow
Write-Host "   (Opzionale - solo se vuoi esporre anche il frontend)" -ForegroundColor Gray
Start-Process powershell -ArgumentList "-NoExit", "-Command", "ngrok http 4200"

Write-Host ""
Write-Host "✅ SERVER AVVIATI!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 PROSSIMI PASSI:" -ForegroundColor Cyan
Write-Host "1. Apri http://localhost:4040 in browser (dashboard ngrok)" -ForegroundColor White
Write-Host "2. Copia gli URL pubblici:" -ForegroundColor White
Write-Host "   • Backend: https://xxxx.ngrok-free.dev (porta 8000)" -ForegroundColor Gray
Write-Host "   • Frontend: https://yyyy.ngrok-free.dev (porta 4200)" -ForegroundColor Gray
Write-Host "3. Aggiorna environment.prod.ts con l'URL pubblico del backend" -ForegroundColor White
Write-Host ""
Write-Host "⚠️  NOTA:" -ForegroundColor Yellow
Write-Host "   • Gli URL ngrok cambiano ogni volta (versione gratuita)" -ForegroundColor Gray
Write-Host "   • Per URL fisso serve account ngrok (gratuito con email)" -ForegroundColor Gray
Write-Host "   • Il backend locale deve essere sempre acceso!" -ForegroundColor Gray
Write-Host ""
Write-Host "💡 Per fermare tutto, chiudi le finestre PowerShell" -ForegroundColor Cyan
Write-Host ""
Write-Host "Premi un tasto per chiudere questa finestra..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

