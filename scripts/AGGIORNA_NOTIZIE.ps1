# Script per aggiornare le notizie - DOPPIO CLIC!
# Aggiorna sia il backend online (Render) che quello locale

Write-Host "📰 Aggiornamento Notizie NewsFlow" -ForegroundColor Cyan
Write-Host ""

# Aggiorna ONLINE (Render)
Write-Host "🌐 Aggiornando notizie su Render (online)..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "https://newsflow-backend-v2.onrender.com/api/admin/collect-news" -Method POST -TimeoutSec 180
    Write-Host "✅ OK ONLINE: $($response.total_articles) notizie aggiornate!" -ForegroundColor Green
    Write-Host "   Messaggio: $($response.message)" -ForegroundColor Gray
} catch {
    Write-Host "❌ ERRORE online: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""

# Aggiorna LOCALE (se backend è attivo)
Write-Host "💻 Aggiornando notizie locali..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/api/admin/collect-news" -Method POST -TimeoutSec 60
    Write-Host "✅ OK LOCALE: $($response.total_articles) notizie aggiornate!" -ForegroundColor Green
    Write-Host "   Messaggio: $($response.message)" -ForegroundColor Gray
} catch {
    Write-Host "⚠️  Backend locale non attivo (normale se non lo stai usando)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "✅ FATTO! Premi un tasto per chiudere..." -ForegroundColor Green
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

