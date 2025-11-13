# Script per riavviare ngrok e esporre il backend locale
# Questo script avvia ngrok per esporre la porta 8000 su internet

Write-Host "🌐 Riavvio Servizio Ngrok" -ForegroundColor Green
Write-Host ""

# Verifica che ngrok sia installato
try {
    $ngrokVersion = ngrok version 2>&1
    Write-Host "✅ Ngrok trovato" -ForegroundColor Green
} catch {
    Write-Host "❌ Ngrok non trovato!" -ForegroundColor Red
    Write-Host "   Installa ngrok da: https://dashboard.ngrok.com/get-started/setup/windows" -ForegroundColor Yellow
    exit 1
}

# Verifica che il backend sia attivo sulla porta 8000
$port8000 = netstat -ano | findstr ":8000" | Select-Object -First 1
if (-not $port8000) {
    Write-Host "⚠️  Nessun servizio trovato sulla porta 8000!" -ForegroundColor Yellow
    Write-Host "   Avvia prima il backend con: .\avvia_backend.ps1" -ForegroundColor Gray
    Write-Host ""
    $continue = Read-Host "Vuoi continuare comunque? (S/N)"
    if ($continue -ne "S" -and $continue -ne "s") {
        exit 1
    }
} else {
    Write-Host "✅ Backend attivo sulla porta 8000" -ForegroundColor Green
}

# Ferma eventuali processi ngrok esistenti
Write-Host ""
Write-Host "🛑 Fermo processi ngrok esistenti..." -ForegroundColor Yellow
Get-Process | Where-Object {$_.ProcessName -eq "ngrok"} | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2

# Verifica configurazione ngrok
Write-Host "🔍 Verifica configurazione ngrok..." -ForegroundColor Yellow
$configCheck = ngrok config check 2>&1
if ($configCheck -match "valid" -or $configCheck -match "authtoken") {
    Write-Host "✅ Ngrok configurato correttamente" -ForegroundColor Green
} else {
    Write-Host "⚠️  Ngrok potrebbe non essere configurato" -ForegroundColor Yellow
    Write-Host "   Configura con: ngrok config add-authtoken YOUR_TOKEN" -ForegroundColor Gray
    Write-Host "   Ottieni il token da: https://dashboard.ngrok.com/get-started/your-authtoken" -ForegroundColor Gray
    Write-Host ""
    $continue = Read-Host "Vuoi continuare comunque? (S/N)"
    if ($continue -ne "S" -and $continue -ne "s") {
        exit 1
    }
}

Write-Host ""
Write-Host "🚀 Avvio tunnel ngrok sulla porta 8000..." -ForegroundColor Cyan
Write-Host ""
Write-Host "📍 Il tuo backend sarà disponibile su un URL pubblico tipo:" -ForegroundColor White
Write-Host "   https://xxxx-xxxx-xxxx.ngrok-free.app" -ForegroundColor Cyan
Write-Host ""
Write-Host "💡 Per vedere l'URL completo:" -ForegroundColor Yellow
Write-Host "   - Apri http://localhost:4040 nel browser (dashboard ngrok)" -ForegroundColor Gray
Write-Host "   - Oppure controlla l'output qui sotto" -ForegroundColor Gray
Write-Host ""
Write-Host "⚠️  Premi CTRL+C per fermare ngrok" -ForegroundColor Yellow
Write-Host ""

# Avvia ngrok in una nuova finestra per vedere l'output
Start-Process -FilePath "ngrok" -ArgumentList "http", "8000" -NoNewWindow

Write-Host "✅ Ngrok avviato!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Prossimi passi:" -ForegroundColor Cyan
Write-Host "   1. Apri http://localhost:4040 per vedere l'URL pubblico" -ForegroundColor White
Write-Host "   2. Copia l'URL ngrok (es: https://xxxx.ngrok-free.app)" -ForegroundColor White
Write-Host "   3. Aggiorna il dominio personalizzato su Vercel se necessario" -ForegroundColor White
Write-Host ""
Write-Host "💡 Per fermare ngrok, chiudi questa finestra o premi CTRL+C" -ForegroundColor Gray

