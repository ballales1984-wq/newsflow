# Script per programmare YouTube Live automatici
# Crea programmazione giornaliera con live a orari specifici

Write-Host "📺 PROGRAMMAZIONE YOUTUBE LIVE AUTOMATICA" -ForegroundColor Cyan
Write-Host ""

Write-Host "🎯 PROGRAMMAZIONE STANDARD:" -ForegroundColor Yellow
Write-Host "   🌅 Mattina: 8:00 (30 min)" -ForegroundColor White
Write-Host "   ☀️  Pranzo: 12:00 (30 min)" -ForegroundColor White
Write-Host "   🌆 Sera: 18:00 (30 min)" -ForegroundColor White
Write-Host "   🌙 Notte: 22:00 (60 min)" -ForegroundColor White
Write-Host ""

$choice = Read-Host "Vuoi creare questa programmazione? (S/N)"

if ($choice -eq "S" -or $choice -eq "s") {
    Write-Host "`n📡 Creo programmazione giornaliera..." -ForegroundColor Yellow
    
    try {
        $response = Invoke-RestMethod -Uri "http://localhost:8000/api/admin/create-daily-schedule" -Method POST -TimeoutSec 30
        
        if ($response.success) {
            Write-Host "`n✅ PROGRAMMAZIONE CREATA!" -ForegroundColor Green
            Write-Host "   Live programmati: $($response.scheduled_streams.Count)" -ForegroundColor White
            Write-Host ""
            
            foreach ($stream in $response.scheduled_streams) {
                $timeSlot = switch ($stream.time_slot) {
                    "morning" { "🌅 Mattina" }
                    "afternoon" { "☀️  Pomeriggio" }
                    "evening" { "🌆 Sera" }
                    "night" { "🌙 Notte" }
                    default { $stream.time_slot }
                }
                Write-Host "   $timeSlot : $($stream.hour):$($stream.minute.ToString('00')) ($($stream.duration_minutes) min)" -ForegroundColor Cyan
            }
            
            Write-Host "`n💡 PROSSIMI PASSI:" -ForegroundColor Yellow
            Write-Host "   1. Il sistema creerà video automaticamente agli orari programmati" -ForegroundColor White
            Write-Host "   2. Configura YouTube Live API per streaming automatico" -ForegroundColor White
            Write-Host "   3. Avvia il scheduler: python backend/youtube_live_scheduler.py" -ForegroundColor White
            Write-Host "`n⚠️  NOTA:" -ForegroundColor Yellow
            Write-Host "   Lo scheduler deve rimanere attivo per eseguire i live automatici" -ForegroundColor White
        } else {
            Write-Host "`n❌ ERRORE:" -ForegroundColor Red
            Write-Host "   $($response.error)" -ForegroundColor White
        }
    } catch {
        Write-Host "`n❌ ERRORE:" -ForegroundColor Red
        Write-Host "   $($_.Exception.Message)" -ForegroundColor White
        Write-Host "`n💡 Assicurati che il backend sia attivo" -ForegroundColor Yellow
    }
} else {
    Write-Host "`n❌ Programmazione annullata" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Premi un tasto per chiudere..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

