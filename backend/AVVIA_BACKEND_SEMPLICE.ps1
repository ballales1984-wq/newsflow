# Script semplice per avviare solo il backend locale
# Per uso interno o con port forwarding sul router

Write-Host "`n=== 🚀 BACKEND LOCALE SEMPLICE ===" -ForegroundColor Cyan
Write-Host ""

$backendDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $backendDir

# CORS per frontend Vercel + locale
$env:CORS_ORIGINS = "https://newsflow-orcin.vercel.app,http://localhost:4200"

Write-Host "🚀 Avvio backend su http://0.0.0.0:8000" -ForegroundColor Green
Write-Host ""
Write-Host "📍 Accessibile da:" -ForegroundColor Cyan
Write-Host "   - http://localhost:8000" -ForegroundColor White
Write-Host "   - http://[TUO_IP_PUBBLICO]:8000 (se configurato port forwarding)" -ForegroundColor White
Write-Host ""
Write-Host "Premi CTRL+C per fermare" -ForegroundColor Gray
Write-Host ""

python -m uvicorn app.main_simple:app --host 0.0.0.0 --port 8000 --reload

