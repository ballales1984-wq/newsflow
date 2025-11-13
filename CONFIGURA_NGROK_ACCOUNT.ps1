# Script per configurare ngrok con account gratuito
# Questo rimuove la pagina di warning che blocca le richieste automatiche

Write-Host "🔧 Configurazione Ngrok con Account Gratuito" -ForegroundColor Cyan
Write-Host ""
Write-Host "📋 Per rimuovere la pagina di warning di ngrok-free:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1️⃣  Crea account gratuito:" -ForegroundColor Cyan
Write-Host "   • Vai su: https://dashboard.ngrok.com/signup" -ForegroundColor White
Write-Host "   • Registrati con email (gratuito)" -ForegroundColor White
Write-Host ""
Write-Host "2️⃣  Ottieni il tuo authtoken:" -ForegroundColor Cyan
Write-Host "   • Vai su: https://dashboard.ngrok.com/get-started/your-authtoken" -ForegroundColor White
Write-Host "   • Accedi al tuo account" -ForegroundColor White
Write-Host "   • Copia il token che vedi" -ForegroundColor White
Write-Host ""
Write-Host "3️⃣  Configura ngrok:" -ForegroundColor Cyan
Write-Host "   • Esegui: ngrok config add-authtoken TUO_TOKEN" -ForegroundColor White
Write-Host ""
Write-Host "4️⃣  Riavvia ngrok:" -ForegroundColor Cyan
Write-Host "   • Ferma ngrok corrente (Ctrl+C)" -ForegroundColor White
Write-Host "   • Riavvia con: ngrok http 8000" -ForegroundColor White
Write-Host ""
Write-Host "✅ Dopo la configurazione:" -ForegroundColor Green
Write-Host "   • La pagina di warning sarà rimossa" -ForegroundColor White
Write-Host "   • Le richieste automatiche funzioneranno" -ForegroundColor White
Write-Host "   • Il frontend Vercel potrà raggiungere il backend" -ForegroundColor White
Write-Host ""
Write-Host "💡 Vuoi configurare ora?" -ForegroundColor Yellow
$risposta = Read-Host "Incolla qui il tuo authtoken ngrok (o premi Invio per saltare)"

if ($risposta -and $risposta.Trim() -ne "") {
    Write-Host ""
    Write-Host "🔧 Configurazione ngrok..." -ForegroundColor Yellow
    try {
        ngrok config add-authtoken $risposta.Trim()
        if ($LASTEXITCODE -eq 0) {
            Write-Host ""
            Write-Host "✅ Ngrok configurato con successo!" -ForegroundColor Green
            Write-Host ""
            Write-Host "🔄 Riavvia ngrok per applicare le modifiche:" -ForegroundColor Cyan
            Write-Host "   1. Ferma ngrok corrente" -ForegroundColor White
            Write-Host "   2. Esegui: ngrok http 8000" -ForegroundColor White
            Write-Host "   3. Oppure usa: .\riavvia_ngrok.ps1" -ForegroundColor White
        } else {
            Write-Host ""
            Write-Host "❌ Errore durante la configurazione" -ForegroundColor Red
        }
    } catch {
        Write-Host ""
        Write-Host "❌ Errore: $_" -ForegroundColor Red
    }
} else {
    Write-Host ""
    Write-Host "⏭️  Configurazione saltata" -ForegroundColor Yellow
    Write-Host "   Puoi configurarlo manualmente più tardi" -ForegroundColor Gray
}

Write-Host ""
Write-Host "Premi un tasto per chiudere..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

