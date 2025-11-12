# Script per creare video per YouTube LIVE (Telegiornale)
# Il video ripete le 85 notizie fino a raggiungere la durata desiderata

Write-Host "📺 CREAZIONE VIDEO PER YOUTUBE LIVE (TELECORONALE)" -ForegroundColor Cyan
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
Write-Host "   - Durata totale 85 notizie: ~18.4 minuti" -ForegroundColor White
Write-Host ""
Write-Host "💡 SCEGLI LA DURATA DEL VIDEO PER LA LIVE:" -ForegroundColor Yellow
Write-Host "   1. 30 minuti (ripete le notizie ~1.6 volte)" -ForegroundColor White
Write-Host "   2. 60 minuti (ripete le notizie ~3.3 volte)" -ForegroundColor White
Write-Host "   3. Durata personalizzata" -ForegroundColor White
Write-Host ""

$scelta = Read-Host "Inserisci il numero (1/2/3)"

$duration_minutes = 30

if ($scelta -eq "1") {
    $duration_minutes = 30
    Write-Host ""
    Write-Host "📹 Creo video di 30 minuti per la live..." -ForegroundColor Yellow
} elseif ($scelta -eq "2") {
    $duration_minutes = 60
    Write-Host ""
    Write-Host "📹 Creo video di 60 minuti per la live..." -ForegroundColor Yellow
} elseif ($scelta -eq "3") {
    Write-Host ""
    $durataInput = Read-Host "Inserisci durata in minuti (es. 45)"
    try {
        $duration_minutes = [int]$durataInput
        Write-Host ""
        Write-Host "📹 Creo video di $duration_minutes minuti per la live..." -ForegroundColor Yellow
    } catch {
        Write-Host "❌ Durata non valida, uso 30 minuti di default" -ForegroundColor Red
        $duration_minutes = 30
    }
} else {
    Write-Host "❌ Scelta non valida, uso 30 minuti di default" -ForegroundColor Red
    $duration_minutes = 30
}

Write-Host ""
Write-Host "⏳ Creazione video in corso..." -ForegroundColor Yellow
Write-Host "   Questo richiederà diversi minuti..." -ForegroundColor Gray
Write-Host ""

# Chiama l'endpoint per creare il video per live
try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/api/admin/create-youtube-live-video?duration_minutes=$duration_minutes" -Method POST -TimeoutSec 3600
    
    Write-Host ""
    Write-Host "✅ VIDEO PER LIVE CREATO CON SUCCESSO!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📊 DETTAGLI:" -ForegroundColor Cyan
    Write-Host "   Durata target: $($response.target_duration_minutes) minuti" -ForegroundColor White
    Write-Host "   Durata reale: $($response.duration_minutes) minuti" -ForegroundColor White
    Write-Host "   Notizie disponibili: $($response.articles_count)" -ForegroundColor White
    Write-Host "   Ripetizioni: ~$($response.repetitions) volte" -ForegroundColor White
    Write-Host "   File: $($response.video_path)" -ForegroundColor White
    Write-Host "   Dimensione: $($response.file_size_mb) MB" -ForegroundColor White
    Write-Host ""
    Write-Host "🎬 COME USARE IL VIDEO PER LA LIVE:" -ForegroundColor Yellow
    Write-Host "   1. Apri YouTube Studio" -ForegroundColor White
    Write-Host "   2. Vai su 'Trasmissioni' > 'Nuova trasmissione'" -ForegroundColor White
    Write-Host "   3. Scegli 'Trasmetti da file'" -ForegroundColor White
    Write-Host "   4. Carica il video: $($response.video_path)" -ForegroundColor White
    Write-Host "   5. Avvia la live!" -ForegroundColor White
    Write-Host ""
    Write-Host "💡 Il video contiene tutte le 85 notizie ripetute fino alla durata desiderata" -ForegroundColor Cyan
    Write-Host "   Ogni notizia dura: durata audio + 1 secondo di pausa" -ForegroundColor Gray
    
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

