# Script PowerShell per avviare il backend locale NewsFlow
# Esegui questo script all'avvio del PC o manualmente

Write-Host "🚀 Avvio Backend NewsFlow..." -ForegroundColor Green
Write-Host ""

# Vai alla directory backend
$backendDir = Join-Path $PSScriptRoot "backend"
if (-not (Test-Path $backendDir)) {
    Write-Host "❌ Directory backend non trovata!" -ForegroundColor Red
    exit 1
}

Set-Location $backendDir

# Ferma eventuali processi esistenti sulla porta 8000
Write-Host "🛑 Verifico processi esistenti sulla porta 8000..." -ForegroundColor Yellow
$processes = Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess -Unique
if ($processes) {
    foreach ($pid in $processes) {
        try {
            Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue
            Write-Host "   ✅ Processo $pid fermato" -ForegroundColor Green
        } catch {
            Write-Host "   ⚠️  Impossibile fermare processo $pid" -ForegroundColor Yellow
        }
    }
    Start-Sleep -Seconds 2
}

# Verifica che Python sia installato
$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonCmd) {
    Write-Host "❌ Python non trovato! Installa Python prima di continuare." -ForegroundColor Red
    exit 1
}

Write-Host "✅ Python trovato: $($pythonCmd.Source)" -ForegroundColor Green

# Avvia il backend con uvicorn
Write-Host ""
Write-Host "▶️  Avvio server backend su http://localhost:8000" -ForegroundColor Cyan
Write-Host "   Premi Ctrl+C per fermare il server" -ForegroundColor Gray
Write-Host ""

# Avvia in background
Start-Process -FilePath "python" -ArgumentList "-m", "uvicorn", "app.main_simple:app", "--host", "0.0.0.0", "--port", "8000", "--reload" -WorkingDirectory $backendDir -NoNewWindow

# Attendi qualche secondo e verifica
Start-Sleep -Seconds 3

try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/api/v1/articles?page=1&size=1" -UseBasicParsing -TimeoutSec 5 -ErrorAction Stop
    $data = $response.Content | ConvertFrom-Json
    Write-Host ""
    Write-Host "✅ Backend avviato correttamente!" -ForegroundColor Green
    Write-Host "   Articoli disponibili: $($data.total)" -ForegroundColor Cyan
    Write-Host "   API disponibile su: http://localhost:8000" -ForegroundColor Cyan
} catch {
    Write-Host ""
    Write-Host "⚠️  Backend in avvio... potrebbe richiedere qualche secondo" -ForegroundColor Yellow
    Write-Host "   Verifica manualmente su: http://localhost:8000/docs" -ForegroundColor Gray
}

Write-Host ""
Write-Host "📝 Per fermare il backend, chiudi questa finestra o usa Ctrl+C" -ForegroundColor Gray

