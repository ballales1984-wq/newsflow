# Script per creare il video TG 4 ore (una volta)
# Usa questo script per creare il video iniziale

Write-Host "📺 CREAZIONE VIDEO TG 4 ORE" -ForegroundColor Cyan
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
Write-Host "   - Per 4 ore servono: ~1105 notizie" -ForegroundColor White
Write-Host "   - Ripetizioni necessarie: ~13 volte" -ForegroundColor White
Write-Host ""
Write-Host "⏳ Creazione video TG 4 ore in corso..." -ForegroundColor Yellow
Write-Host "   Questo richiederà molto tempo (30-60 minuti)..." -ForegroundColor Gray
Write-Host "   ⚠️  NON CHIUDERE QUESTA FINESTRA!" -ForegroundColor Red
Write-Host ""

# Chiama l'endpoint per creare il video TG 4 ore
try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/api/admin/create-tg-4h-video" -Method POST -TimeoutSec 7200
    
    Write-Host ""
    Write-Host "✅ VIDEO TG 4 ORE CREATO CON SUCCESSO!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📊 DETTAGLI:" -ForegroundColor Cyan
    Write-Host "   Durata target: $($response.target_duration_minutes) minuti (4 ore)" -ForegroundColor White
    Write-Host "   Durata reale: $($response.duration_minutes) minuti" -ForegroundColor White
    Write-Host "   Notizie disponibili: $($response.articles_count)" -ForegroundColor White
    Write-Host "   Ripetizioni: ~$($response.repetitions) volte" -ForegroundColor White
    Write-Host "   File: $($response.video_path)" -ForegroundColor White
    Write-Host "   Dimensione: $($response.file_size_mb) MB" -ForegroundColor White
    Write-Host ""
    Write-Host "🎬 PROSSIMI PASSI:" -ForegroundColor Yellow
    Write-Host "   1. Carica il video su YouTube Studio > Trasmissioni" -ForegroundColor White
    Write-Host "   2. Avvia la live con il video" -ForegroundColor White
    Write-Host "   3. Avvia AVVIA_SYNC_TG.ps1 per mantenere il video sempre aggiornato" -ForegroundColor White
    Write-Host ""
    Write-Host "💡 Il sistema rigenererà automaticamente il video quando le notizie vengono aggiornate" -ForegroundColor Cyan
    
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

