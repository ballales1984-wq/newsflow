# Script per creare video YouTube automatici
# DOPPIO CLIC per creare video!

Write-Host "🎬 CREAZIONE VIDEO YOUTUBE..." -ForegroundColor Cyan
Write-Host ""

# Parametri
$maxArticles = 5
if ($args.Count -gt 0) {
    $maxArticles = [int]$args[0]
}

Write-Host "📹 Creo video con $maxArticles notizie..." -ForegroundColor Yellow
Write-Host "⏳ Questo richiederà alcuni minuti..." -ForegroundColor Gray
Write-Host ""

# Chiama endpoint backend
try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/api/admin/create-youtube-video?max_articles=$maxArticles" -Method POST -TimeoutSec 600
    
    if ($response.success) {
        Write-Host "✅ SUCCESSO!" -ForegroundColor Green
        Write-Host "   Video creato: $($response.video_path)" -ForegroundColor White
        Write-Host "   Notizie incluse: $($response.articles_count)" -ForegroundColor White
        Write-Host "   Dimensione: $($response.file_size_mb) MB" -ForegroundColor White
        Write-Host ""
        Write-Host "💡 PROSSIMI PASSI:" -ForegroundColor Cyan
        Write-Host "   1. Il video è salvato in: backend/youtube_videos/" -ForegroundColor White
        Write-Host "   2. Puoi caricarlo manualmente su YouTube" -ForegroundColor White
        Write-Host "   3. Oppure configura YouTube API per upload automatico" -ForegroundColor White
    } else {
        Write-Host "❌ ERRORE:" -ForegroundColor Red
        Write-Host "   $($response.error)" -ForegroundColor White
        if ($response.hint) {
            Write-Host ""
            Write-Host "💡 SUGGERIMENTO:" -ForegroundColor Yellow
            Write-Host "   $($response.hint)" -ForegroundColor White
        }
    }
} catch {
    Write-Host "❌ ERRORE:" -ForegroundColor Red
    Write-Host "   $($_.Exception.Message)" -ForegroundColor White
    Write-Host ""
    Write-Host "💡 Assicurati che:" -ForegroundColor Yellow
    Write-Host "   - Il backend sia attivo su http://localhost:8000" -ForegroundColor White
    Write-Host "   - Le dipendenze siano installate: pip install moviepy gtts pillow" -ForegroundColor White
}

Write-Host ""
Write-Host "Premi un tasto per chiudere..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

