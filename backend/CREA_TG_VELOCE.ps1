# Script per creare video TG veloce (~18-20 minuti)
# Include tutte le 85 notizie con immagini

Write-Host "📺 CREAZIONE VIDEO TG VELOCE (~20 minuti)" -ForegroundColor Cyan
Write-Host ""

# Verifica che il backend sia attivo
Write-Host "📡 Verifico backend..." -ForegroundColor Yellow
try {
    $health = Invoke-RestMethod -Uri "http://localhost:8000/api/health" -TimeoutSec 3
    Write-Host "✅ Backend attivo!" -ForegroundColor Green
} catch {
    Write-Host "❌ Backend non attivo!" -ForegroundColor Red
    Write-Host "   Avvia il backend prima di creare il video" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Premi un tasto per chiudere..." -ForegroundColor Gray
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}

Write-Host ""
Write-Host "📊 CALCOLI:" -ForegroundColor Cyan
Write-Host "   - Notizie disponibili: 85" -ForegroundColor White
Write-Host "   - Durata per notizia: ~13 secondi (audio + 1s pausa)" -ForegroundColor White
Write-Host "   - Durata totale: ~18-20 minuti" -ForegroundColor White
Write-Host "   - Tempo creazione: ~10-15 minuti (molto più veloce!)" -ForegroundColor Green
Write-Host ""
Write-Host "⏳ Creazione video TG in corso..." -ForegroundColor Yellow
Write-Host "   Questo richiederà ~10-15 minuti..." -ForegroundColor Gray
Write-Host ""

# Chiama l'endpoint per creare il video TG
try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/api/admin/create-tg-video" -Method POST -TimeoutSec 1800
    
    Write-Host ""
    Write-Host "✅ VIDEO TG CREATO CON SUCCESSO!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📊 DETTAGLI:" -ForegroundColor Cyan
    Write-Host "   Durata: $($response.duration_minutes) minuti" -ForegroundColor White
    Write-Host "   Notizie incluse: $($response.articles_count)" -ForegroundColor White
    Write-Host "   File: $($response.video_path)" -ForegroundColor White
    Write-Host "   Dimensione: $($response.file_size_mb) MB" -ForegroundColor White
    Write-Host ""
    Write-Host "🎬 PROSSIMI PASSI:" -ForegroundColor Yellow
    Write-Host "   1. Programma live multiple: .\PROGRAMMA_LIVE_MULTIPLE.ps1" -ForegroundColor White
    Write-Host "   2. Avvia scheduler: .\AVVIA_SCHEDULER_LIVE.ps1" -ForegroundColor White
    Write-Host "   3. Le live si accenderanno e spegneranno automaticamente!" -ForegroundColor White
    Write-Host ""
    Write-Host "💡 Ogni live dura ~20 minuti e include tutte le 85 notizie" -ForegroundColor Cyan
    
} catch {
    Write-Host ""
    Write-Host "❌ ERRORE nella creazione del video:" -ForegroundColor Red
    Write-Host "   $($_.Exception.Message)" -ForegroundColor Yellow
    if ($_.Exception.Response) {
        $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
        $responseBody = $reader.ReadToEnd()
        Write-Host "   Dettagli: $responseBody" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "Premi un tasto per chiudere..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

