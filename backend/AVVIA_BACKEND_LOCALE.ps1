# Script per avviare il backend FastAPI sul PC locale come server pubblico
# Il backend sarà accessibile da qualsiasi dispositivo sulla stessa rete o tramite ngrok

Write-Host "`n=== 🚀 AVVIO BACKEND LOCALE ===" -ForegroundColor Cyan
Write-Host ""

# Verifica che Python sia installato
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python trovato: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python non trovato! Installa Python 3.9+ da python.org" -ForegroundColor Red
    exit 1
}

# Vai alla directory backend
$backendDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $backendDir

Write-Host "📁 Directory: $backendDir" -ForegroundColor Yellow
Write-Host ""

# Verifica che le dipendenze siano installate
Write-Host "🔍 Verifica dipendenze..." -ForegroundColor Yellow
try {
    python -c "import fastapi, uvicorn" 2>&1 | Out-Null
    Write-Host "✅ Dipendenze installate" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Installazione dipendenze..." -ForegroundColor Yellow
    pip install -r requirements.txt
}

Write-Host ""

# Ottieni IP locale
$localIP = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.IPAddress -like "192.168.*" -or $_.IPAddress -like "10.*"} | Select-Object -First 1).IPAddress
if (-not $localIP) {
    $localIP = "localhost"
}

# Configura CORS per accettare:
# - Frontend Vercel (https://newsflow-orcin.vercel.app)
# - Frontend locale (http://localhost:4200)
# - Qualsiasi dispositivo sulla rete locale
$corsOrigins = "https://newsflow-orcin.vercel.app,http://localhost:4200,http://$localIP:4200,http://$localIP:8000"

Write-Host "🌐 Configurazione CORS:" -ForegroundColor Cyan
Write-Host "   - Frontend Vercel: https://newsflow-orcin.vercel.app" -ForegroundColor Gray
Write-Host "   - Frontend locale: http://localhost:4200" -ForegroundColor Gray
Write-Host "   - IP locale: http://$localIP:8000" -ForegroundColor Gray
Write-Host ""

# Imposta variabile d'ambiente CORS
$env:CORS_ORIGINS = $corsOrigins

Write-Host "🚀 Avvio server FastAPI..." -ForegroundColor Green
Write-Host ""
Write-Host "📍 URL Backend:" -ForegroundColor Cyan
Write-Host "   - Locale: http://localhost:8000" -ForegroundColor White
Write-Host "   - Rete locale: http://$localIP:8000" -ForegroundColor White
Write-Host ""
Write-Host "📋 Endpoint disponibili:" -ForegroundColor Cyan
Write-Host "   - Health: http://localhost:8000/api/health" -ForegroundColor Gray
Write-Host "   - Articoli: http://localhost:8000/api/v1/articles" -ForegroundColor Gray
Write-Host "   - Debug: http://localhost:8000/api/debug/files" -ForegroundColor Gray
Write-Host ""
Write-Host "⚠️  IMPORTANTE:" -ForegroundColor Yellow
Write-Host "   Per esporre il server su Internet, usa ngrok:" -ForegroundColor Yellow
Write-Host "   ngrok http 8000" -ForegroundColor White
Write-Host ""
Write-Host "   Poi aggiorna il frontend con l'URL ngrok" -ForegroundColor Yellow
Write-Host ""
Write-Host "Premi CTRL+C per fermare il server" -ForegroundColor Gray
Write-Host ""

# Avvia il server
python -m uvicorn app.main_simple:app --host 0.0.0.0 --port 8000 --reload

