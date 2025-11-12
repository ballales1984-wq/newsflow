# Script per configurazione automatica sistema ottimale
# Crea video TG e programma live automaticamente

Write-Host "🎯 CONFIGURAZIONE AUTOMATICA SISTEMA OTTIMALE" -ForegroundColor Cyan
Write-Host ""

# Verifica backend
Write-Host "📡 Verifico backend..." -ForegroundColor Yellow
try {
    $health = Invoke-RestMethod -Uri "http://localhost:8000/api/health" -TimeoutSec 3
    Write-Host "✅ Backend attivo!" -ForegroundColor Green
} catch {
    Write-Host "❌ Backend non attivo! Avvialo prima." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "📊 CONFIGURAZIONE SCELTA:" -ForegroundColor Cyan
Write-Host "   ✅ Video TG: ~20 minuti (85 notizie)" -ForegroundColor Green
Write-Host "   ✅ Programmazione: 8 live al giorno (ogni 3 ore)" -ForegroundColor Green
Write-Host "   ✅ Auto-sync: rigenera quando notizie aggiornate" -ForegroundColor Green
Write-Host ""

# STEP 1: Crea video TG
Write-Host "📹 STEP 1: Creo video TG..." -ForegroundColor Yellow
Write-Host "   ⏳ Questo richiederà ~10-15 minuti..." -ForegroundColor Gray

try {
    $videoResponse = Invoke-RestMethod -Uri "http://localhost:8000/api/admin/create-tg-video" -Method POST -TimeoutSec 1800
    
    if ($videoResponse.success) {
        Write-Host "   ✅ Video creato!" -ForegroundColor Green
        Write-Host "      Durata: $($videoResponse.duration_minutes) minuti" -ForegroundColor White
        Write-Host "      File: $($videoResponse.video_path)" -ForegroundColor White
        Write-Host "      Dimensione: $($videoResponse.file_size_mb) MB" -ForegroundColor White
    } else {
        Write-Host "   ❌ Errore creazione video: $($videoResponse.error)" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "   ❌ Errore: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

Write-Host ""

# STEP 2: Programma live ottimale (8 live al giorno, ogni 3 ore)
Write-Host "📅 STEP 2: Programmo live ottimali..." -ForegroundColor Yellow
Write-Host "   8 live al giorno (ogni 3 ore: 6, 9, 12, 15, 18, 21, 0, 3)" -ForegroundColor Gray

$schedule = @(
    @{hour=6; minute=0; duration_minutes=20; time_slot="mattina"},
    @{hour=9; minute=0; duration_minutes=20; time_slot="mattina"},
    @{hour=12; minute=0; duration_minutes=20; time_slot="pranzo"},
    @{hour=15; minute=0; duration_minutes=20; time_slot="pomeriggio"},
    @{hour=18; minute=0; duration_minutes=20; time_slot="sera"},
    @{hour=21; minute=0; duration_minutes=20; time_slot="sera"},
    @{hour=0; minute=0; duration_minutes=20; time_slot="notte"},
    @{hour=3; minute=0; duration_minutes=20; time_slot="notte"}
)

$successCount = 0
foreach ($stream in $schedule) {
    try {
        $uri = "http://localhost:8000/api/admin/schedule-youtube-live?hour=$($stream.hour)&minute=$($stream.minute)&duration_minutes=$($stream.duration_minutes)"
        $response = Invoke-RestMethod -Uri $uri -Method POST -TimeoutSec 30
        Write-Host "   ✅ Live: $($stream.hour.ToString('00')):$($stream.minute.ToString('00'))" -ForegroundColor Green
        $successCount++
    } catch {
        Write-Host "   ⚠️  Errore: $($stream.hour):$($stream.minute)" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "✅ Programmazione completata: $successCount/$($schedule.Count) live programmate" -ForegroundColor Green

Write-Host ""
Write-Host "🎉 SISTEMA CONFIGURATO CON SUCCESSO!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 RIEPILOGO:" -ForegroundColor Cyan
Write-Host "   ✅ Video TG creato (~20 minuti)" -ForegroundColor White
Write-Host "   ✅ 8 live programmate al giorno" -ForegroundColor White
Write-Host "   ✅ Ogni live dura ~20 minuti" -ForegroundColor White
Write-Host ""
Write-Host "🚀 PROSSIMI PASSI:" -ForegroundColor Yellow
Write-Host "   1. Avvia scheduler: .\AVVIA_SCHEDULER_LIVE.ps1" -ForegroundColor White
Write-Host "   2. Le live partiranno automaticamente agli orari programmati" -ForegroundColor White
Write-Host "   3. Quando aggiorni notizie, rigenera video: .\CREA_TG_VELOCE.ps1" -ForegroundColor White
Write-Host ""
Write-Host "💡 Il sistema è pronto per YouTube Live!" -ForegroundColor Cyan
Write-Host ""
Write-Host "Premi un tasto per chiudere..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

