# Script per creare video YouTube con TUTTE le notizie disponibili
# La durata viene calcolata automaticamente: durata audio + 1 secondo di pausa per ogni notizia

Write-Host "🎬 CREAZIONE VIDEO YOUTUBE CON TUTTE LE NOTIZIE" -ForegroundColor Cyan
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
Write-Host "📹 Creo video con TUTTE le notizie disponibili..." -ForegroundColor Yellow
Write-Host "   Ogni notizia avrà durata = durata audio + 1 secondo di pausa" -ForegroundColor Gray
Write-Host ""

# Chiama l'endpoint per creare il video
try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/api/admin/create-youtube-video?max_articles=999" -Method POST -TimeoutSec 1800
    Write-Host ""
    Write-Host "✅ VIDEO CREATO CON SUCCESSO!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📊 DETTAGLI:" -ForegroundColor Cyan
    Write-Host "   Articoli inclusi: $($response.articles_count)" -ForegroundColor White
    Write-Host "   File: $($response.video_path)" -ForegroundColor White
    Write-Host "   Dimensione: $($response.file_size_mb) MB" -ForegroundColor White
    if ($response.duration_minutes) {
        Write-Host "   Durata: $($response.duration_minutes) minuti" -ForegroundColor White
    }
    Write-Host ""
    Write-Host "🎉 Il video è pronto per essere caricato su YouTube!" -ForegroundColor Green
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

