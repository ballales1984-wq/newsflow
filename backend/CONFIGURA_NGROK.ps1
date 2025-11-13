# Script interattivo per configurare ngrok con il token

Write-Host "`n=== 🔧 CONFIGURAZIONE NGROK ===" -ForegroundColor Cyan
Write-Host ""

# Verifica che ngrok.exe esista
if (-not (Test-Path "ngrok.exe")) {
    Write-Host "❌ ngrok.exe non trovato in questa cartella!" -ForegroundColor Red
    Write-Host "   Assicurati di essere in: C:\Users\user\news\backend" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ ngrok.exe trovato" -ForegroundColor Green
Write-Host ""

# Istruzioni
Write-Host "📝 Per ottenere il token ngrok:" -ForegroundColor Yellow
Write-Host "   1. Vai su: https://dashboard.ngrok.com/get-started/your-authtoken" -ForegroundColor Cyan
Write-Host "   2. Accedi o registrati (gratuito)" -ForegroundColor White
Write-Host "   3. Copia il token che vedi" -ForegroundColor White
Write-Host ""

# Chiedi il token
$token = Read-Host "Incolla qui il tuo token ngrok"

if ([string]::IsNullOrWhiteSpace($token)) {
    Write-Host "❌ Token vuoto!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "🔧 Configurazione ngrok con il token..." -ForegroundColor Yellow

# Esegui il comando
try {
    $result = .\ngrok.exe config add-authtoken $token 2>&1
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅✅✅ NGROK CONFIGURATO CON SUCCESSO!" -ForegroundColor Green
        Write-Host ""
        Write-Host "🚀 Ora puoi avviare il backend con ngrok:" -ForegroundColor Cyan
        Write-Host "   .\AVVIA_BACKEND_NGROK.ps1" -ForegroundColor White
    } else {
        Write-Host "❌ Errore durante la configurazione:" -ForegroundColor Red
        Write-Host $result -ForegroundColor Yellow
    }
} catch {
    Write-Host "❌ Errore: $_" -ForegroundColor Red
}

