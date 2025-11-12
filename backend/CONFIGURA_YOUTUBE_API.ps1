# Script per configurare YouTube API credentials
# Necessario per upload e live automatici

Write-Host "🔧 CONFIGURAZIONE YOUTUBE API" -ForegroundColor Cyan
Write-Host ""

Write-Host "📋 PASSAGGI PER OTTENERE LE CREDENZIALI:" -ForegroundColor Yellow
Write-Host ""

Write-Host "1️⃣  VAI SU GOOGLE CLOUD CONSOLE" -ForegroundColor Cyan
Write-Host "   https://console.cloud.google.com/" -ForegroundColor White
Write-Host ""

Write-Host "2️⃣  CREA UN PROGETTO (se non ce l'hai)" -ForegroundColor Cyan
Write-Host "   - Clicca su 'Seleziona progetto' > 'Nuovo progetto'" -ForegroundColor White
Write-Host "   - Nome: NewsFlow YouTube" -ForegroundColor White
Write-Host "   - Crea" -ForegroundColor White
Write-Host ""

Write-Host "3️⃣  ABILITA YOUTUBE DATA API V3" -ForegroundColor Cyan
Write-Host "   - Vai su 'API e servizi' > 'Libreria'" -ForegroundColor White
Write-Host "   - Cerca 'YouTube Data API v3'" -ForegroundColor White
Write-Host "   - Clicca 'Abilita'" -ForegroundColor White
Write-Host ""

Write-Host "4️⃣  CREA CREDENZIALI OAuth 2.0" -ForegroundColor Cyan
Write-Host "   - Vai su 'API e servizi' > 'Credenziali'" -ForegroundColor White
Write-Host "   - Clicca 'Crea credenziali' > 'ID client OAuth 2.0'" -ForegroundColor White
Write-Host "   - Tipo applicazione: 'App desktop'" -ForegroundColor White
Write-Host "   - Nome: NewsFlow YouTube Client" -ForegroundColor White
Write-Host "   - Crea" -ForegroundColor White
Write-Host ""

Write-Host "5️⃣  SCARICA IL FILE JSON" -ForegroundColor Cyan
Write-Host "   - Clicca sul client OAuth creato" -ForegroundColor White
Write-Host "   - Clicca 'Scarica JSON'" -ForegroundColor White
Write-Host "   - Salva come: backend\youtube_credentials.json" -ForegroundColor White
Write-Host ""

Write-Host "6️⃣  CONFIGURA CONSENT SCREEN" -ForegroundColor Cyan
Write-Host "   - Vai su 'Schermata di consenso OAuth'" -ForegroundColor White
Write-Host "   - Tipo utente: 'Esterno'" -ForegroundColor White
Write-Host "   - Compila nome app: NewsFlow" -ForegroundColor White
Write-Host "   - Salva e continua" -ForegroundColor White
Write-Host ""

Write-Host "✅ DOPO AVER SCARICATO IL FILE:" -ForegroundColor Green
Write-Host "   - Metti il file in: backend\youtube_credentials.json" -ForegroundColor White
Write-Host "   - Esegui: .\CONFIGURA_SISTEMA_OTTIMALE.ps1" -ForegroundColor White
Write-Host "   - Alla prima esecuzione si aprirà il browser per autorizzare" -ForegroundColor White
Write-Host ""

Write-Host "💡 IMPORTANTE:" -ForegroundColor Yellow
Write-Host "   - La prima volta devi autorizzare l'app nel browser" -ForegroundColor White
Write-Host "   - Dopo l'autorizzazione, tutto sarà automatico!" -ForegroundColor White
Write-Host ""

$hasFile = Test-Path "backend\youtube_credentials.json"
if ($hasFile) {
    Write-Host "✅ File youtube_credentials.json trovato!" -ForegroundColor Green
    Write-Host "   Puoi procedere con la configurazione!" -ForegroundColor White
} else {
    Write-Host "⚠️  File youtube_credentials.json NON trovato" -ForegroundColor Yellow
    Write-Host "   Segui i passaggi sopra per scaricarlo" -ForegroundColor White
}

Write-Host ""
Write-Host "Premi un tasto per chiudere..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

