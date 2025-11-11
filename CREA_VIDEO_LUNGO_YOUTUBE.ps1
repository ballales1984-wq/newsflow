# Script per creare video lunghi per playlist YouTube 24/7
# Crea video di 1-2 ore da aggiungere a playlist YouTube

Write-Host "🎬 CREAZIONE VIDEO LUNGO PER PLAYLIST YOUTUBE 24/7" -ForegroundColor Cyan
Write-Host ""

# Parametri
$durationMinutes = 60  # Durata default: 1 ora
if ($args.Count -gt 0) {
    $durationMinutes = [int]$args[0]
}

Write-Host "📹 Creo video di $durationMinutes minuti..." -ForegroundColor Yellow
Write-Host "⏳ Questo richiederà molto tempo (10-30 minuti)..." -ForegroundColor Gray
Write-Host "💡 Il video conterrà ~$($durationMinutes * 4) notizie" -ForegroundColor Cyan
Write-Host ""

# Chiama endpoint backend
try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/api/admin/create-youtube-video-long?duration_minutes=$durationMinutes" -Method POST -TimeoutSec 3600
    
    if ($response.success) {
        Write-Host "✅ SUCCESSO!" -ForegroundColor Green
        Write-Host "   Video creato: $($response.video_path)" -ForegroundColor White
        Write-Host "   Durata: $($response.duration_minutes) minuti" -ForegroundColor White
        Write-Host "   Notizie incluse: $($response.articles_count)" -ForegroundColor White
        Write-Host "   Dimensione: $($response.file_size_mb) MB" -ForegroundColor White
        Write-Host ""
        Write-Host "💡 PROSSIMI PASSI:" -ForegroundColor Cyan
        Write-Host "   1. Carica il video su YouTube" -ForegroundColor White
        Write-Host "   2. Aggiungi alla playlist YouTube 24/7" -ForegroundColor White
        Write-Host "   3. Imposta la playlist su 'Riproduci in loop'" -ForegroundColor White
        Write-Host "   4. YouTube riprodurrà automaticamente la playlist!" -ForegroundColor White
    } else {
        Write-Host "❌ ERRORE:" -ForegroundColor Red
        Write-Host "   $($response.error)" -ForegroundColor White
    }
} catch {
    Write-Host "❌ ERRORE:" -ForegroundColor Red
    Write-Host "   $($_.Exception.Message)" -ForegroundColor White
    Write-Host ""
    Write-Host "💡 Assicurati che:" -ForegroundColor Yellow
    Write-Host "   - Il backend sia attivo su http://localhost:8000" -ForegroundColor White
    Write-Host "   - Le dipendenze siano installate" -ForegroundColor White
}

Write-Host ""
Write-Host "Premi un tasto per chiudere..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

