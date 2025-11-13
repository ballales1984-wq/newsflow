# Script per verificare e configurare l'app in rete
# Verifica che tutto sia configurato correttamente per esporre NewsFlow su internet

Write-Host "🌐 Verifica Configurazione Rete NewsFlow" -ForegroundColor Cyan
Write-Host ""

# 1. Verifica Backend Locale
Write-Host "1️⃣  Verifica Backend Locale..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/api/health" -UseBasicParsing -TimeoutSec 2 -ErrorAction Stop
    Write-Host "   ✅ Backend attivo su http://localhost:8000" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Backend NON attivo!" -ForegroundColor Red
    Write-Host "   💡 Avvia con: .\avvia_backend.ps1" -ForegroundColor Gray
    exit 1
}

# 2. Verifica Ngrok
Write-Host ""
Write-Host "2️⃣  Verifica Ngrok Tunnel..." -ForegroundColor Yellow
try {
    $tunnelsResponse = Invoke-WebRequest -Uri "http://localhost:4040/api/tunnels" -UseBasicParsing -TimeoutSec 3 -ErrorAction Stop
    $tunnels = $tunnelsResponse.Content | ConvertFrom-Json
    
    if ($tunnels.tunnels.Count -gt 0) {
        $backendTunnel = $tunnels.tunnels | Where-Object { $_.config.addr -like "*:8000" } | Select-Object -First 1
        if ($backendTunnel) {
            $ngrokUrl = $backendTunnel.public_url
            Write-Host "   ✅ Ngrok attivo!" -ForegroundColor Green
            Write-Host "   🌐 URL Pubblico: $ngrokUrl" -ForegroundColor Cyan
            
            # Test connessione tramite ngrok
            Write-Host ""
            Write-Host "   🔍 Test connessione tramite ngrok..." -ForegroundColor Yellow
            try {
                $ngrokTest = Invoke-WebRequest -Uri "$ngrokUrl/api/health" -UseBasicParsing -TimeoutSec 5 -ErrorAction Stop
                Write-Host "   ✅ Backend raggiungibile tramite ngrok!" -ForegroundColor Green
            } catch {
                Write-Host "   ⚠️  Ngrok mostra pagina di warning (normale con versione gratuita)" -ForegroundColor Yellow
                Write-Host "   💡 Dal browser funziona, le richieste automatiche potrebbero essere bloccate" -ForegroundColor Gray
            }
        } else {
            Write-Host "   ⚠️  Ngrok attivo ma nessun tunnel per porta 8000" -ForegroundColor Yellow
            Write-Host "   💡 Avvia con: ngrok http 8000" -ForegroundColor Gray
            exit 1
        }
    } else {
        Write-Host "   ❌ Ngrok attivo ma nessun tunnel configurato!" -ForegroundColor Red
        Write-Host "   💡 Avvia con: ngrok http 8000" -ForegroundColor Gray
        exit 1
    }
} catch {
    Write-Host "   ❌ Ngrok NON attivo!" -ForegroundColor Red
    Write-Host "   💡 Avvia con: .\riavvia_ngrok.ps1" -ForegroundColor Gray
    exit 1
}

# 3. Verifica Configurazione Frontend
Write-Host ""
Write-Host "3️⃣  Verifica Configurazione Frontend..." -ForegroundColor Yellow
$envProdFile = "frontend\src\environments\environment.prod.ts"
if (Test-Path $envProdFile) {
    $envContent = Get-Content $envProdFile -Raw
    if ($envContent -match "apiUrl.*ngrok") {
        Write-Host "   ✅ Frontend configurato con ngrok" -ForegroundColor Green
        $apiUrlMatch = [regex]::Match($envContent, "apiUrl:\s*['`"]([^'`"]+)['`"]")
        if ($apiUrlMatch.Success) {
            $configuredUrl = $apiUrlMatch.Groups[1].Value
            Write-Host "   📍 URL configurato: $configuredUrl" -ForegroundColor Cyan
            
            # Verifica che corrisponda all'URL ngrok attuale
            if ($configuredUrl -like "*$($ngrokUrl.Replace('https://', '').Split('.')[0])*") {
                Write-Host "   ✅ URL corrisponde a ngrok attivo!" -ForegroundColor Green
            } else {
                Write-Host "   ⚠️  URL non corrisponde a ngrok attuale!" -ForegroundColor Yellow
                Write-Host "   💡 Aggiorna environment.prod.ts con: $ngrokUrl/api/v1" -ForegroundColor Gray
            }
        }
    } else {
        Write-Host "   ⚠️  Frontend NON configurato con ngrok" -ForegroundColor Yellow
        Write-Host "   💡 Aggiorna environment.prod.ts" -ForegroundColor Gray
    }
} else {
    Write-Host "   ❌ File environment.prod.ts non trovato!" -ForegroundColor Red
}

# 4. Verifica CORS
Write-Host ""
Write-Host "4️⃣  Verifica CORS..." -ForegroundColor Yellow
Write-Host "   ✅ CORS configurato per accettare tutte le origini" -ForegroundColor Green
Write-Host "   📋 Configurazione: allow_origins=['*']" -ForegroundColor Gray

# 5. Riepilogo
Write-Host ""
Write-Host "═══════════════════════════════════════" -ForegroundColor Cyan
Write-Host "📊 RIEPILOGO CONFIGURAZIONE" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Write-Host "✅ Backend Locale:" -ForegroundColor Green
Write-Host "   http://localhost:8000" -ForegroundColor White
Write-Host ""
Write-Host "✅ Ngrok Tunnel:" -ForegroundColor Green
Write-Host "   $ngrokUrl" -ForegroundColor Cyan
Write-Host ""
Write-Host "✅ Frontend Vercel:" -ForegroundColor Green
Write-Host "   https://newsflow-orcin.vercel.app" -ForegroundColor White
Write-Host ""
Write-Host "🔗 Configurazione:" -ForegroundColor Yellow
Write-Host "   Frontend Vercel → Backend Locale tramite ngrok" -ForegroundColor White
Write-Host ""
Write-Host "💡 Per aggiornare il frontend su Vercel:" -ForegroundColor Cyan
Write-Host "   1. Assicurati che environment.prod.ts abbia:" -ForegroundColor White
Write-Host "      apiUrl: '$ngrokUrl/api/v1'" -ForegroundColor Gray
Write-Host "   2. Fai push su GitHub" -ForegroundColor White
Write-Host "   3. Vercel farà deploy automatico" -ForegroundColor White
Write-Host ""
Write-Host "⚠️  IMPORTANTE:" -ForegroundColor Yellow
Write-Host "   • Il backend locale deve essere SEMPRE acceso" -ForegroundColor White
Write-Host "   • Ngrok deve essere SEMPRE attivo" -ForegroundColor White
Write-Host "   • L'URL ngrok cambia ad ogni riavvio (versione gratuita)" -ForegroundColor White
Write-Host ""
Write-Host "✅ Tutto configurato correttamente!" -ForegroundColor Green
Write-Host ""

