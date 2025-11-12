# Script per creare video corti da 2 minuti ogni 20 minuti
# Seleziona solo notizie con immagini e usa voce narrante femminile

Write-Host "📹 CREAZIONE VIDEO CORTO DA 2 MINUTI" -ForegroundColor Cyan
Write-Host "   Solo notizie con immagini + voce narrante femminile" -ForegroundColor Gray
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
Write-Host "📊 CARATTERISTICHE VIDEO:" -ForegroundColor Cyan
Write-Host "   - Durata: 2 minuti" -ForegroundColor White
Write-Host "   - Solo notizie con immagini" -ForegroundColor White
Write-Host "   - Voce narrante femminile italiana" -ForegroundColor White
Write-Host "   - Perfetto per live ogni 20 minuti" -ForegroundColor White
Write-Host ""
Write-Host "⏳ Creazione video in corso..." -ForegroundColor Yellow
Write-Host "   Questo richiederà alcuni minuti..." -ForegroundColor Gray
Write-Host ""

# Chiama l'endpoint per creare il video corto
try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/api/admin/create-youtube-short-video" -Method POST -TimeoutSec 1800
    
    Write-Host ""
    Write-Host "✅ VIDEO CORTO CREATO CON SUCCESSO!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📊 DETTAGLI:" -ForegroundColor Cyan
    Write-Host "   Durata target: $($response.target_duration_minutes) minuti" -ForegroundColor White
    Write-Host "   Durata reale: $($response.duration_minutes) minuti" -ForegroundColor White
    Write-Host "   Articoli totali: $($response.articles_count)" -ForegroundColor White
    Write-Host "   File: $($response.video_path)" -ForegroundColor White
    Write-Host "   Dimensione: $($response.file_size_mb) MB" -ForegroundColor White
    Write-Host ""
    Write-Host "🎬 VIDEO PRONTO PER LIVE!" -ForegroundColor Yellow
    Write-Host "   Puoi caricarlo su YouTube per la live" -ForegroundColor White
    Write-Host ""
    Write-Host "💡 Per programmare live ogni 20 minuti:" -ForegroundColor Cyan
    Write-Host "   Esegui: .\PROGRAMMA_LIVE_20MIN.ps1" -ForegroundColor White
    
} catch {
    Write-Host ""
    Write-Host "❌ ERRORE nella creazione del video:" -ForegroundColor Red
    Write-Host "   $($_.Exception.Message)" -ForegroundColor Yellow
    if ($_.Exception.Response) {
        try {
            $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
            $responseBody = $reader.ReadToEnd()
            Write-Host "   Dettagli: $responseBody" -ForegroundColor Yellow
        } catch {
            # Ignora errori di lettura stream
        }
    }
}

Write-Host ""
Write-Host "Premi un tasto per chiudere..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

