# Script per programmare live YouTube ogni 20 minuti
# Crea video corti da 2 minuti e programma live automatiche

Write-Host "📺 PROGRAMMAZIONE LIVE YOUTUBE OGNI 20 MINUTI" -ForegroundColor Cyan
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
Write-Host "📊 PROGRAMMAZIONE:" -ForegroundColor Cyan
Write-Host "   - Video corti da 2 minuti" -ForegroundColor White
Write-Host "   - Live ogni 20 minuti (00:00, 00:20, 00:40, 01:00, ...)" -ForegroundColor White
Write-Host "   - Totale: 72 live al giorno" -ForegroundColor White
Write-Host "   - Solo notizie con immagini" -ForegroundColor White
Write-Host "   - Voce narrante femminile" -ForegroundColor White
Write-Host ""

$conferma = Read-Host "Vuoi programmare le live ogni 20 minuti? (S/N)"

if ($conferma -ne "S" -and $conferma -ne "s") {
    Write-Host "❌ Operazione annullata" -ForegroundColor Yellow
    exit 0
}

Write-Host ""
Write-Host "⏳ Creo programmazione..." -ForegroundColor Yellow

# Crea programmazione: ogni 20 minuti per 24 ore
$schedule = @()
for ($hour = 0; $hour -lt 24; $hour++) {
    for ($minute = 0; $minute -lt 60; $minute += 20) {
        $schedule += @{
            hour = $hour
            minute = $minute
            duration_minutes = 2
            time_slot = "auto"
        }
    }
}

Write-Host "   Totale live programmate: $($schedule.Count)" -ForegroundColor White
Write-Host ""

# Programma ogni live
$successCount = 0
foreach ($stream in $schedule) {
    try {
        $uri = "http://localhost:8000/api/admin/schedule-youtube-live?hour=$($stream.hour)&minute=$($stream.minute)&duration_minutes=$($stream.duration_minutes)"
        $response = Invoke-RestMethod -Uri $uri -Method POST -TimeoutSec 30
        $successCount++
        
        if ($successCount % 10 -eq 0) {
            Write-Host "   ✅ Programmato: $successCount/$($schedule.Count)" -ForegroundColor Green
        }
    } catch {
        Write-Host "   ⚠️  Errore programmazione $($stream.hour):$($stream.minute): $($_.Exception.Message)" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "✅ PROGRAMMAZIONE COMPLETATA!" -ForegroundColor Green
Write-Host "   Live programmate: $successCount/$($schedule.Count)" -ForegroundColor White
Write-Host ""
Write-Host "📋 PROSSIMI PASSI:" -ForegroundColor Cyan
Write-Host "   1. Avvia scheduler: .\AVVIA_SCHEDULER_LIVE_20MIN.ps1" -ForegroundColor White
Write-Host "   2. Lo scheduler creerà i video automaticamente ogni 20 minuti" -ForegroundColor White
Write-Host "   3. I video verranno caricati su YouTube automaticamente" -ForegroundColor White
Write-Host ""
Write-Host "💡 NOTA:" -ForegroundColor Yellow
Write-Host "   Ogni 20 minuti verrà creato un nuovo video da 2 minuti" -ForegroundColor White
Write-Host "   con le notizie più recenti che hanno immagini" -ForegroundColor White

Write-Host ""
Write-Host "Premi un tasto per chiudere..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

