# Script per programmare live multiple durante il giorno
# Ogni live dura ~20 minuti (tutte le 85 notizie)

Write-Host "📺 PROGRAMMAZIONE LIVE MULTIPLE" -ForegroundColor Cyan
Write-Host ""

# Verifica che il backend sia attivo
Write-Host "📡 Verifico backend..." -ForegroundColor Yellow
try {
    $health = Invoke-RestMethod -Uri "http://localhost:8000/api/health" -TimeoutSec 3
    Write-Host "✅ Backend attivo!" -ForegroundColor Green
} catch {
    Write-Host "❌ Backend non attivo!" -ForegroundColor Red
    Write-Host "   Avvia il backend prima di programmare le live" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Premi un tasto per chiudere..." -ForegroundColor Gray
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}

Write-Host ""
Write-Host "📊 CONFIGURAZIONE LIVE:" -ForegroundColor Cyan
Write-Host "   - Durata ogni live: ~20 minuti (85 notizie)" -ForegroundColor White
Write-Host "   - Le live si accendono e spengono automaticamente" -ForegroundColor White
Write-Host ""
Write-Host "💡 SCEGLI LA PROGRAMMAZIONE:" -ForegroundColor Yellow
Write-Host "   1. Programmazione standard (6 live al giorno)" -ForegroundColor White
Write-Host "   2. Programmazione intensiva (12 live al giorno)" -ForegroundColor White
Write-Host "   3. Programmazione personalizzata" -ForegroundColor White
Write-Host ""

$scelta = Read-Host "Inserisci il numero (1/2/3)"

if ($scelta -eq "1") {
    Write-Host ""
    Write-Host "📅 Creo programmazione standard (6 live al giorno)..." -ForegroundColor Yellow
    Write-Host "   Ogni live dura ~20 minuti" -ForegroundColor Gray
    Write-Host ""
    
    # Programmazione standard: 6 live al giorno
    $schedule = @(
        @{hour=8; minute=0; duration_minutes=20; time_slot="mattina"},
        @{hour=10; minute=0; duration_minutes=20; time_slot="mattina"},
        @{hour=12; minute=0; duration_minutes=20; time_slot="pranzo"},
        @{hour=15; minute=0; duration_minutes=20; time_slot="pomeriggio"},
        @{hour=18; minute=0; duration_minutes=20; time_slot="sera"},
        @{hour=21; minute=0; duration_minutes=20; time_slot="sera"}
    )
    
    foreach ($stream in $schedule) {
        try {
            $uri = "http://localhost:8000/api/admin/schedule-youtube-live?hour=$($stream.hour)&minute=$($stream.minute)&duration_minutes=$($stream.duration_minutes)"
            $response = Invoke-RestMethod -Uri $uri -Method POST -TimeoutSec 30
            Write-Host "   ✅ Live programmata: $($stream.hour.ToString('00')):$($stream.minute.ToString('00')) ($($stream.time_slot))" -ForegroundColor Green
        } catch {
            Write-Host "   ❌ Errore: $($stream.hour):$($stream.minute) - $($_.Exception.Message)" -ForegroundColor Red
        }
    }
    
    Write-Host ""
    Write-Host "✅ Programmazione completata! Totale: $($schedule.Count) live" -ForegroundColor Green
    
} elseif ($scelta -eq "2") {
    Write-Host ""
    Write-Host "📅 Creo programmazione intensiva (12 live al giorno)..." -ForegroundColor Yellow
    Write-Host "   Ogni live dura ~20 minuti" -ForegroundColor Gray
    Write-Host ""
    
    # Programmazione intensiva: 12 live al giorno (ogni 2 ore)
    $schedule = @()
    for ($h = 6; $h -le 23; $h += 2) {
        $schedule += @{hour=$h; minute=0; duration_minutes=20; time_slot="auto"}
    }
    
    foreach ($stream in $schedule) {
        try {
            $uri = "http://localhost:8000/api/admin/schedule-youtube-live?hour=$($stream.hour)&minute=$($stream.minute)&duration_minutes=$($stream.duration_minutes)"
            $response = Invoke-RestMethod -Uri $uri -Method POST -TimeoutSec 30
            Write-Host "   ✅ Live programmata: $($stream.hour.ToString('00')):$($stream.minute.ToString('00'))" -ForegroundColor Green
        } catch {
            Write-Host "   ❌ Errore: $($stream.hour):$($stream.minute) - $($_.Exception.Message)" -ForegroundColor Red
        }
    }
    
    Write-Host ""
    Write-Host "✅ Programmazione completata! Totale: $($schedule.Count) live" -ForegroundColor Green
    
} elseif ($scelta -eq "3") {
    Write-Host ""
    Write-Host "📝 Programmazione personalizzata" -ForegroundColor Yellow
    Write-Host ""
    
    $streams = @()
    $continua = "S"
    
    while ($continua -eq "S" -or $continua -eq "s") {
        Write-Host "--- Nuova Live ---" -ForegroundColor Cyan
        
        $ora = Read-Host "Ora (0-23)"
        $minuto = Read-Host "Minuto (0-59)"
        $durata = Read-Host "Durata in minuti (default: 20)"
        
        if ([string]::IsNullOrWhiteSpace($durata)) {
            $durata = 20
        }
        
        try {
            $oraInt = [int]$ora
            $minutoInt = [int]$minuto
            $durataInt = [int]$durata
            
            $uri = "http://localhost:8000/api/admin/schedule-youtube-live?hour=$oraInt&minute=$minutoInt&duration_minutes=$durataInt"
            $response = Invoke-RestMethod -Uri $uri -Method POST -TimeoutSec 30
            
            Write-Host "✅ Live programmata alle $($ora):$($minuto) (durata: $durata min)" -ForegroundColor Green
            $streams += $response.scheduled_stream
        } catch {
            Write-Host "❌ ERRORE:" -ForegroundColor Red
            Write-Host "   $($_.Exception.Message)" -ForegroundColor Yellow
        }
        
        Write-Host ""
        $continua = Read-Host "Vuoi aggiungere un'altra live? (S/N)"
    }
    
    Write-Host ""
    Write-Host "✅ Programmazione completata! Totale: $($streams.Count) live" -ForegroundColor Green
    
} else {
    Write-Host "❌ Scelta non valida!" -ForegroundColor Red
}

Write-Host ""
Write-Host "🎬 PROSSIMI PASSI:" -ForegroundColor Yellow
Write-Host "   1. Crea il video TG: .\CREA_TG_VELOCE.ps1" -ForegroundColor White
Write-Host "   2. Avvia scheduler: .\AVVIA_SCHEDULER_LIVE.ps1" -ForegroundColor White
Write-Host "   3. Le live partiranno automaticamente agli orari programmati!" -ForegroundColor White
Write-Host ""
Write-Host "💡 Ogni live:" -ForegroundColor Cyan
Write-Host "   - Dura ~20 minuti" -ForegroundColor Gray
Write-Host "   - Include tutte le 85 notizie" -ForegroundColor Gray
Write-Host "   - Si accende e spegne automaticamente" -ForegroundColor Gray
Write-Host ""
Write-Host "Premi un tasto per chiudere..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

