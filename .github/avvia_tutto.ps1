# Script principale per avviare tutto NewsFlow all'avvio del PC
# Questo script:
# 1. Avvia il backend locale
# 2. (Opzionale) Sincronizza e fa deploy su Vercel

Write-Host "╔════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║   NewsFlow - Avvio Completo Sistema   ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

$rootDir = $PSScriptRoot

# 1. Avvia backend locale
Write-Host "🔧 STEP 1: Avvio Backend Locale" -ForegroundColor Yellow
Write-Host "─────────────────────────────────────────" -ForegroundColor Gray
& (Join-Path $rootDir "avvia_backend.ps1")

Write-Host ""
Write-Host ""

# 2. Chiedi se fare deploy su Vercel
Write-Host "🌐 STEP 2: Deploy su Vercel (Opzionale)" -ForegroundColor Yellow
Write-Host "─────────────────────────────────────────" -ForegroundColor Gray
$deploy = Read-Host "Vuoi sincronizzare e fare deploy su Vercel? (S/N)"

if ($deploy -eq "S" -or $deploy -eq "s" -or $deploy -eq "Y" -or $deploy -eq "y") {
    & (Join-Path $rootDir "sincronizza_e_deploy.ps1")
} else {
    Write-Host "   ⏭️  Deploy saltato" -ForegroundColor Gray
}

Write-Host ""
Write-Host "✅ Sistema NewsFlow avviato!" -ForegroundColor Green
Write-Host ""
Write-Host "📝 Servizi attivi:" -ForegroundColor Cyan
Write-Host "   • Backend locale: http://localhost:8000" -ForegroundColor White
Write-Host "   • API Docs: http://localhost:8000/docs" -ForegroundColor White
Write-Host ""
Write-Host "💡 Per fermare il backend, chiudi questa finestra" -ForegroundColor Gray

