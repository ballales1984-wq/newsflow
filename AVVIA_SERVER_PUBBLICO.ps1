# Script per avviare backend + frontend + ngrok
# Salva come: AVVIA_SERVER_PUBBLICO.ps1

Write-Host "🚀 Avvio server pubblico..." -ForegroundColor Cyan
Write-Host ""

# Verifica se ngrok è installato
$ngrokPath = Get-Command ngrok -ErrorAction SilentlyContinue
if (-not $ngrokPath) {
    Write-Host "❌ ngrok non trovato!" -ForegroundColor Red
    Write-Host "`n📥 INSTALLAZIONE:" -ForegroundColor Yellow
    Write-Host "1. Scarica da: https://ngrok.com/download" -ForegroundColor White
    Write-Host "2. Estrai ngrok.exe in una cartella (es: C:\ngrok\)" -ForegroundColor White
    Write-Host "3. Aggiungi al PATH o metti ngrok.exe nella cartella news" -ForegroundColor White
    Write-Host "`nOPPURE usa: choco install ngrok (se hai Chocolatey)" -ForegroundColor Gray
    exit
}

Write-Host "✅ ngrok trovato!" -ForegroundColor Green
Write-Host ""

# Avvia backend
Write-Host "🔧 Avvio backend su porta 8000..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd C:\Users\user\news\backend; .\venv\Scripts\uvicorn.exe app.main_simple:app --host 0.0.0.0 --port 8000"
Start-Sleep -Seconds 3

# Avvia frontend
Write-Host "🔧 Avvio frontend su porta 4200..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd C:\Users\user\news\frontend; npm start"
Start-Sleep -Seconds 5

# Avvia ngrok per backend
Write-Host "🌐 Avvio ngrok per backend (porta 8000)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "ngrok http 8000"
Start-Sleep -Seconds 3

# Avvia ngrok per frontend
Write-Host "🌐 Avvio ngrok per frontend (porta 4200)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "ngrok http 4200"

Write-Host ""
Write-Host "✅ SERVER AVVIATI!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 PROSSIMI PASSI:" -ForegroundColor Cyan
Write-Host "1. Apri http://localhost:4040 in browser (dashboard ngrok)" -ForegroundColor White
Write-Host "2. Copia gli URL pubblici (es: https://xxxx.ngrok.io)" -ForegroundColor White
Write-Host "3. Aggiorna environment.ts con l'URL pubblico del backend" -ForegroundColor White
Write-Host ""
Write-Host "⚠️  NOTA: Gli URL ngrok cambiano ogni volta (versione gratuita)" -ForegroundColor Yellow
Write-Host "   Per URL fisso serve account ngrok (gratuito con email)" -ForegroundColor Gray
Write-Host ""
Write-Host "Premi un tasto per chiudere..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

