# Script per avviare backend locale + ngrok tunnel pubblico
# Questo crea un URL pubblico gratuito per il tuo backend

Write-Host "`n=== 🌐 BACKEND LOCALE + NGROK ===" -ForegroundColor Cyan
Write-Host ""

# Verifica che ngrok sia installato
try {
    $ngrokVersion = ngrok version 2>&1
    Write-Host "✅ ngrok trovato: $ngrokVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ ngrok non trovato!" -ForegroundColor Red
    Write-Host ""
    Write-Host "📥 Installa ngrok:" -ForegroundColor Yellow
    Write-Host "   1. Scarica da: https://ngrok.com/download" -ForegroundColor White
    Write-Host "   2. Estrai ngrok.exe nella cartella backend" -ForegroundColor White
    Write-Host "   3. Oppure aggiungi ngrok al PATH di sistema" -ForegroundColor White
    Write-Host ""
    Write-Host "   OPPURE usa: choco install ngrok" -ForegroundColor Cyan
    Write-Host ""
    exit 1
}

# Vai alla directory backend
$backendDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $backendDir

# Configura CORS per includere ngrok
$corsOrigins = "https://newsflow-orcin.vercel.app,http://localhost:4200"

Write-Host "🔧 Configurazione CORS..." -ForegroundColor Yellow
$env:CORS_ORIGINS = $corsOrigins

Write-Host ""
Write-Host "🚀 Avvio backend in background..." -ForegroundColor Green

# Avvia backend in background
$backendJob = Start-Job -ScriptBlock {
    Set-Location $using:backendDir
    $env:CORS_ORIGINS = $using:corsOrigins
    python -m uvicorn app.main_simple:app --host 0.0.0.0 --port 8000
}

# Attendi che il backend sia pronto
Write-Host "⏳ Attendo avvio backend..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

# Verifica che il backend sia attivo
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/api/health" -TimeoutSec 2 -UseBasicParsing
    Write-Host "✅ Backend attivo!" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Backend potrebbe non essere ancora pronto, continuo comunque..." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🌐 Avvio tunnel ngrok..." -ForegroundColor Green
Write-Host ""
Write-Host "📍 Il tuo backend sarà disponibile su un URL pubblico tipo:" -ForegroundColor Cyan
Write-Host "   https://xxxx-xxxx-xxxx.ngrok-free.app" -ForegroundColor White
Write-Host ""
Write-Host "⚠️  IMPORTANTE:" -ForegroundColor Yellow
Write-Host "   1. Copia l'URL ngrok che apparirà" -ForegroundColor White
Write-Host "   2. Aggiorna frontend/src/environments/environment.prod.ts con:" -ForegroundColor White
Write-Host "      apiUrl: 'https://xxxx-xxxx-xxxx.ngrok-free.app/api/v1'" -ForegroundColor Gray
Write-Host "   3. Ricompila il frontend: ng build --configuration production" -ForegroundColor White
Write-Host ""
Write-Host "Premi CTRL+C per fermare tutto" -ForegroundColor Gray
Write-Host ""

# Avvia ngrok
ngrok http 8000

# Quando ngrok si chiude, ferma anche il backend
Write-Host "`n🛑 Chiusura backend..." -ForegroundColor Yellow
Stop-Job $backendJob
Remove-Job $backendJob

Write-Host "✅ Tutto fermato!" -ForegroundColor Green

