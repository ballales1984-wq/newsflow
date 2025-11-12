# Script per creare video corto da 2 minuti usando backend Render
# Non richiede backend locale attivo

Write-Host "CREAZIONE VIDEO CORTO DA 2 MINUTI" -ForegroundColor Cyan
Write-Host "Usando backend Render (online)" -ForegroundColor Gray
Write-Host ""

# URL backend Render
$backendUrl = "https://newsflow-backend-v2.onrender.com"

Write-Host "Verifico backend Render..." -ForegroundColor Yellow
try {
    $health = Invoke-RestMethod -Uri "$backendUrl/api/health" -TimeoutSec 30
    Write-Host "Backend Render attivo!" -ForegroundColor Green
} catch {
    Write-Host "Backend Render non risponde!" -ForegroundColor Red
    Write-Host "Errore: $($_.Exception.Message)" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Il backend potrebbe essere in risveglio..." -ForegroundColor Yellow
    Write-Host "Aspetta 30-60 secondi e riprova" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Premi un tasto per chiudere..." -ForegroundColor Gray
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}

Write-Host ""
Write-Host "CARATTERISTICHE VIDEO:" -ForegroundColor Cyan
Write-Host "  - Durata: 2 minuti" -ForegroundColor White
Write-Host "  - Solo notizie con immagini" -ForegroundColor White
Write-Host "  - Voce narrante femminile italiana" -ForegroundColor White
Write-Host "  - Perfetto per live ogni 20 minuti" -ForegroundColor White
Write-Host ""
Write-Host "Creazione video in corso..." -ForegroundColor Yellow
Write-Host "Questo richiedera alcuni minuti..." -ForegroundColor Gray
Write-Host "Il backend Render potrebbe impiegare 30-60 secondi per risvegliarsi" -ForegroundColor Gray
Write-Host ""

# Chiama l'endpoint per creare il video corto
try {
    $response = Invoke-RestMethod -Uri "$backendUrl/api/admin/create-youtube-short-video" -Method POST -TimeoutSec 1800
    
    Write-Host ""
    Write-Host "VIDEO CORTO CREATO CON SUCCESSO!" -ForegroundColor Green
    Write-Host ""
    Write-Host "DETTAGLI:" -ForegroundColor Cyan
    if ($response.success) {
        Write-Host "  Durata target: $($response.target_duration_minutes) minuti" -ForegroundColor White
        Write-Host "  Durata reale: $($response.duration_minutes) minuti" -ForegroundColor White
        Write-Host "  Articoli totali: $($response.articles_count)" -ForegroundColor White
        Write-Host "  File: $($response.video_path)" -ForegroundColor White
        Write-Host "  Dimensione: $($response.file_size_mb) MB" -ForegroundColor White
        Write-Host ""
        Write-Host "VIDEO PRONTO!" -ForegroundColor Yellow
        Write-Host "Il video e stato creato sul server Render" -ForegroundColor White
        Write-Host "Percorso: $($response.video_path)" -ForegroundColor White
    } else {
        Write-Host "  Errore: $($response.error)" -ForegroundColor Red
    }
    
} catch {
    Write-Host ""
    Write-Host "ERRORE nella creazione del video:" -ForegroundColor Red
    Write-Host "  $($_.Exception.Message)" -ForegroundColor Yellow
    if ($_.Exception.Response) {
        try {
            $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
            $responseBody = $reader.ReadToEnd()
            Write-Host "  Dettagli: $responseBody" -ForegroundColor Yellow
        } catch {
            # Ignora errori di lettura stream
        }
    }
    Write-Host ""
    Write-Host "POSSIBILI CAUSE:" -ForegroundColor Cyan
    Write-Host "  - Backend Render in risveglio (aspetta 30-60 secondi)" -ForegroundColor White
    Write-Host "  - Dipendenze mancanti sul server (moviepy, gTTS)" -ForegroundColor White
    Write-Host "  - Errore nella generazione video" -ForegroundColor White
}

Write-Host ""
Write-Host "Premi un tasto per chiudere..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
