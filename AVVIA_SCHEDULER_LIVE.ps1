# Script per avviare lo scheduler YouTube Live
# Mantieni questo script attivo per eseguire i live automatici

Write-Host "🔄 AVVIO SCHEDULER YOUTUBE LIVE" -ForegroundColor Cyan
Write-Host ""
Write-Host "⚠️  IMPORTANTE:" -ForegroundColor Yellow
Write-Host "   - Questo script deve rimanere ATTIVO" -ForegroundColor White
Write-Host "   - I live partiranno automaticamente agli orari programmati" -ForegroundColor White
Write-Host "   - Non chiudere questa finestra!" -ForegroundColor White
Write-Host ""

$confirm = Read-Host "Vuoi avviare lo scheduler? (S/N)"

if ($confirm -eq "S" -or $confirm -eq "s") {
    Write-Host "`n🚀 Avvio scheduler..." -ForegroundColor Green
    Write-Host "   (Premi Ctrl+C per fermare)" -ForegroundColor Gray
    Write-Host ""
    
    cd backend
    python youtube_live_scheduler.py
} else {
    Write-Host "`n❌ Scheduler annullato" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Premi un tasto per chiudere..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

