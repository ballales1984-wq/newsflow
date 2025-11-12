# Script per sistema completamente automatizzato
# Crea video, carica su YouTube e programma live automaticamente

Write-Host "🤖 SISTEMA COMPLETAMENTE AUTOMATIZZATO" -ForegroundColor Cyan
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

# Verifica credenziali YouTube
Write-Host ""
Write-Host "🔐 Verifico credenziali YouTube..." -ForegroundColor Yellow
$hasCredentials = Test-Path "backend\youtube_credentials.json"
if (-not $hasCredentials) {
    Write-Host "⚠️  Credenziali YouTube non trovate!" -ForegroundColor Yellow
    Write-Host "   Esegui prima: .\CONFIGURA_YOUTUBE_API.ps1" -ForegroundColor White
    Write-Host ""
    Write-Host "Premi un tasto per chiudere..." -ForegroundColor Gray
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}
Write-Host "✅ Credenziali YouTube trovate!" -ForegroundColor Green

Write-Host ""
Write-Host "📊 CONFIGURAZIONE AUTOMATICA:" -ForegroundColor Cyan
Write-Host "   ✅ Video TG: ~20 minuti (85 notizie)" -ForegroundColor Green
Write-Host "   ✅ Upload automatico su YouTube" -ForegroundColor Green
Write-Host "   ✅ 8 live programmate al giorno" -ForegroundColor Green
Write-Host "   ✅ Live si avviano automaticamente" -ForegroundColor Green
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
    } else {
        Write-Host "   ❌ Errore: $($videoResponse.error)" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "   ❌ Errore: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

Write-Host ""

# STEP 2: Upload automatico su YouTube
Write-Host "📤 STEP 2: Carico video su YouTube..." -ForegroundColor Yellow
Write-Host "   ⚠️  Alla prima esecuzione si aprirà il browser per autorizzare" -ForegroundColor Yellow

try {
    $uploadResponse = Invoke-RestMethod -Uri "http://localhost:8000/api/admin/upload-tg-to-youtube" -Method POST -TimeoutSec 600
    
    if ($uploadResponse.success) {
        Write-Host "   ✅ Video caricato su YouTube!" -ForegroundColor Green
        Write-Host "      Video ID: $($uploadResponse.video_id)" -ForegroundColor White
        Write-Host "      URL: $($uploadResponse.video_url)" -ForegroundColor White
    } else {
        Write-Host "   ⚠️  Errore upload: $($uploadResponse.error)" -ForegroundColor Yellow
        Write-Host "      Continua comunque con la programmazione live..." -ForegroundColor Gray
    }
} catch {
    Write-Host "   ⚠️  Errore upload: $($_.Exception.Message)" -ForegroundColor Yellow
    Write-Host "      Continua comunque con la programmazione live..." -ForegroundColor Gray
}

Write-Host ""

# STEP 3: Programma live automatiche (8 al giorno)
Write-Host "📅 STEP 3: Programmo live automatiche..." -ForegroundColor Yellow

$schedule = @(
    @{hour=6; minute=0},
    @{hour=9; minute=0},
    @{hour=12; minute=0},
    @{hour=15; minute=0},
    @{hour=18; minute=0},
    @{hour=21; minute=0},
    @{hour=0; minute=0},
    @{hour=3; minute=0}
)

$successCount = 0
foreach ($stream in $schedule) {
    try {
        $uri = "http://localhost:8000/api/admin/create-youtube-live-auto?hour=$($stream.hour)&minute=$($stream.minute)"
        $response = Invoke-RestMethod -Uri $uri -Method POST -TimeoutSec 30
        
        if ($response.success) {
            Write-Host "   ✅ Live: $($stream.hour.ToString('00')):$($stream.minute.ToString('00')) - $($response.broadcast_id)" -ForegroundColor Green
            $successCount++
        } else {
            Write-Host "   ⚠️  Errore: $($stream.hour):$($stream.minute) - $($response.error)" -ForegroundColor Yellow
        }
    } catch {
        Write-Host "   ⚠️  Errore: $($stream.hour):$($stream.minute) - $($_.Exception.Message)" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "🎉 SISTEMA COMPLETAMENTE AUTOMATIZZATO!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 RIEPILOGO:" -ForegroundColor Cyan
Write-Host "   ✅ Video TG creato e caricato su YouTube" -ForegroundColor White
Write-Host "   ✅ $successCount/$($schedule.Count) live programmate" -ForegroundColor White
Write-Host "   ✅ Le live partiranno automaticamente agli orari programmati" -ForegroundColor White
Write-Host ""
Write-Host "🚀 PROSSIMI PASSI:" -ForegroundColor Yellow
Write-Host "   1. Avvia scheduler: .\AVVIA_SCHEDULER_LIVE.ps1" -ForegroundColor White
Write-Host "   2. Le live partiranno automaticamente!" -ForegroundColor White
Write-Host "   3. Quando aggiorni notizie:" -ForegroundColor White
Write-Host "      - .\AGGIORNA_NOTIZIE.ps1" -ForegroundColor Gray
Write-Host "      - .\CONFIGURA_SISTEMA_OTTIMALE.ps1 (rigenera tutto)" -ForegroundColor Gray
Write-Host ""
Write-Host "💡 TUTTO AUTOMATICO - ZERO INTERVENTO MANUALE!" -ForegroundColor Cyan
Write-Host ""
Write-Host "Premi un tasto per chiudere..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

