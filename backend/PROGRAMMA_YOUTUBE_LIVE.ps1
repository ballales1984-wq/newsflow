# Script interattivo per configurare la programmazione YouTube Live
# Configura insieme all'utente gli orari per i live automatici

Write-Host "📺 CONFIGURAZIONE PROGRAMMAZIONE YOUTUBE LIVE" -ForegroundColor Cyan
Write-Host ""

# Verifica che il backend sia attivo
Write-Host "📡 Verifico backend..." -ForegroundColor Yellow
try {
    $health = Invoke-RestMethod -Uri "http://localhost:8000/api/health" -TimeoutSec 3
    Write-Host "✅ Backend attivo!" -ForegroundColor Green
} catch {
    Write-Host "❌ Backend non attivo!" -ForegroundColor Red
    Write-Host "   Avvia il backend prima di configurare la programmazione" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Premi un tasto per chiudere..." -ForegroundColor Gray
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}

Write-Host ""
Write-Host "📋 Hai 85 notizie disponibili da leggere" -ForegroundColor Yellow
Write-Host ""
Write-Host "Scegli come vuoi programmare i live:" -ForegroundColor Cyan
Write-Host "   1. Programmazione standard (4 live al giorno)" -ForegroundColor White
Write-Host "   2. Programmazione personalizzata" -ForegroundColor White
Write-Host "   3. Visualizza programmazione attuale" -ForegroundColor White
Write-Host ""

$scelta = Read-Host "Inserisci il numero (1/2/3)"

if ($scelta -eq "1") {
    Write-Host ""
    Write-Host "📅 Creo programmazione standard..." -ForegroundColor Yellow
    Write-Host "   - 08:00 (mattina, 30 min)" -ForegroundColor Gray
    Write-Host "   - 12:00 (pranzo, 30 min)" -ForegroundColor Gray
    Write-Host "   - 18:00 (sera, 30 min)" -ForegroundColor Gray
    Write-Host "   - 22:00 (notte, 60 min)" -ForegroundColor Gray
    Write-Host ""
    
    try {
        $response = Invoke-RestMethod -Uri "http://localhost:8000/api/admin/create-daily-schedule" -Method POST -TimeoutSec 30
        Write-Host "✅ Programmazione creata!" -ForegroundColor Green
        Write-Host ""
        Write-Host "📊 DETTAGLI:" -ForegroundColor Cyan
        Write-Host "   Live programmati: $($response.total_streams)" -ForegroundColor White
        Write-Host ""
        Write-Host "🎬 PROSSIMI PASSI:" -ForegroundColor Yellow
        Write-Host "   1. Avvia AVVIA_SCHEDULER_LIVE.ps1 per eseguire i live automatici" -ForegroundColor White
        Write-Host "   2. Lo scheduler creerà i video automaticamente agli orari programmati" -ForegroundColor White
        Write-Host "   3. I video verranno creati con tutte le notizie disponibili" -ForegroundColor White
    } catch {
        Write-Host "❌ ERRORE:" -ForegroundColor Red
        Write-Host "   $($_.Exception.Message)" -ForegroundColor Yellow
    }
    
} elseif ($scelta -eq "2") {
    Write-Host ""
    Write-Host "📝 Programmazione personalizzata" -ForegroundColor Yellow
    Write-Host ""
    
    $streams = @()
    $continua = "S"
    
    while ($continua -eq "S" -or $continua -eq "s") {
        Write-Host "--- Nuovo Live ---" -ForegroundColor Cyan
        
        $ora = Read-Host "Ora (0-23)"
        $minuto = Read-Host "Minuto (0-59)"
        $durata = Read-Host "Durata in minuti (es. 30)"
        
        try {
            $oraInt = [int]$ora
            $minutoInt = [int]$minuto
            $durataInt = [int]$durata
            
            $uri = "http://localhost:8000/api/admin/schedule-youtube-live?hour=$oraInt&minute=$minutoInt&duration_minutes=$durataInt"
            $response = Invoke-RestMethod -Uri $uri -Method POST -TimeoutSec 30
            
            Write-Host "✅ Live programmato alle $($ora):$($minuto) (durata: $durata min)" -ForegroundColor Green
            $streams += $response.scheduled_stream
        } catch {
            Write-Host "❌ ERRORE:" -ForegroundColor Red
            Write-Host "   $($_.Exception.Message)" -ForegroundColor Yellow
        }
        
        Write-Host ""
        $continua = Read-Host "Vuoi aggiungere un altro live? (S/N)"
    }
    
    Write-Host ""
    Write-Host "✅ Programmazione completata!" -ForegroundColor Green
    Write-Host "   Totale live: $($streams.Count)" -ForegroundColor White
    
} elseif ($scelta -eq "3") {
    Write-Host ""
    Write-Host "📋 Programmazione attuale:" -ForegroundColor Yellow
    Write-Host ""
    
    try {
        $response = Invoke-RestMethod -Uri "http://localhost:8000/api/admin/youtube-schedule" -Method GET -TimeoutSec 30
        
        if ($response.scheduled_streams.Count -eq 0) {
            Write-Host "⚠️  Nessuna programmazione trovata" -ForegroundColor Yellow
            Write-Host "   Usa l'opzione 1 o 2 per crearne una" -ForegroundColor Gray
        } else {
            Write-Host "📺 LIVE PROGRAMMATI:" -ForegroundColor Cyan
            foreach ($stream in $response.scheduled_streams) {
                $timeSlot = $stream.time_slot
                $hour = $stream.hour.ToString("00")
                $minute = $stream.minute.ToString("00")
                $duration = $stream.duration_minutes
                Write-Host "   $hour`:$minute ($timeSlot) - Durata: $duration min" -ForegroundColor White
            }
            Write-Host ""
            Write-Host "Totale: $($response.scheduled_streams.Count) live" -ForegroundColor Green
        }
    } catch {
        Write-Host "❌ ERRORE:" -ForegroundColor Red
        Write-Host "   $($_.Exception.Message)" -ForegroundColor Yellow
    }
    
} else {
    Write-Host "❌ Scelta non valida!" -ForegroundColor Red
}

Write-Host ""
Write-Host "💡 RICORDA:" -ForegroundColor Yellow
Write-Host "   - Ogni notizia avrà durata = durata audio + 1 secondo di pausa" -ForegroundColor Gray
Write-Host "   - I video vengono creati automaticamente agli orari programmati" -ForegroundColor Gray
Write-Host "   - Avvia AVVIA_SCHEDULER_LIVE.ps1 per eseguire i live" -ForegroundColor Gray
Write-Host ""
Write-Host "Premi un tasto per chiudere..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

