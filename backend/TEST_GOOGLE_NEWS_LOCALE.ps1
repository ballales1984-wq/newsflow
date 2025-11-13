# Script per testare Google News localmente
# Avvia il backend, esegue la raccolta e verifica i risultati

Write-Host "`n=== TEST GOOGLE NEWS LOCALE ===" -ForegroundColor Cyan
Write-Host ""

$backendDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $backendDir

# Verifica che Python sia disponibile
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python trovato: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python non trovato!" -ForegroundColor Red
    exit 1
}

# Verifica se il backend è già in esecuzione
Write-Host "`nVerifica backend locale..." -ForegroundColor Yellow
$backendRunning = $false
try {
    $health = Invoke-RestMethod -Uri "http://localhost:8000/api/health" -TimeoutSec 2 -ErrorAction Stop
    Write-Host "✅ Backend già attivo su http://localhost:8000" -ForegroundColor Green
    $backendRunning = $true
} catch {
    Write-Host "⚠️  Backend non attivo, avvio..." -ForegroundColor Yellow
    
    # Avvia backend in background
    $env:CORS_ORIGINS = "https://newsflow-orcin.vercel.app,http://localhost:4200"
    $backendProcess = Start-Process -FilePath "python" -ArgumentList "-m", "uvicorn", "app.main_simple:app", "--host", "127.0.0.1", "--port", "8000" -PassThru -WindowStyle Hidden
    
    Write-Host 'Attendo avvio backend (10 secondi)...' -ForegroundColor Yellow
    Start-Sleep -Seconds 10
    
    # Verifica che sia partito
    $retries = 0
    $maxRetries = 6
    while ($retries -lt $maxRetries) {
        try {
            $health = Invoke-RestMethod -Uri "http://localhost:8000/api/health" -TimeoutSec 2 -ErrorAction Stop
            Write-Host "✅ Backend avviato con successo!" -ForegroundColor Green
            $backendRunning = $true
            break
        } catch {
            $retries++
            if ($retries -lt $maxRetries) {
                Write-Host "   Tentativo $retries/$maxRetries..." -ForegroundColor Gray
                Start-Sleep -Seconds 5
            } else {
                Write-Host "❌ Impossibile avviare il backend" -ForegroundColor Red
                if ($backendProcess) {
                    Stop-Process -Id $backendProcess.Id -Force -ErrorAction SilentlyContinue
                }
                exit 1
            }
        }
    }
}

if (-not $backendRunning) {
    Write-Host "❌ Backend non disponibile" -ForegroundColor Red
    exit 1
}

# Esegui raccolta notizie
Write-Host "`nEsecuzione raccolta notizie con Google News..." -ForegroundColor Cyan
Write-Host "   (Questo può richiedere alcuni minuti)" -ForegroundColor Gray
Write-Host ""

try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/api/admin/collect-news" -Method POST -TimeoutSec 600
    Write-Host "✅ Raccolta completata!" -ForegroundColor Green
    Write-Host "   Totale articoli: $($response.total_articles)" -ForegroundColor Cyan
    Write-Host "   Messaggio: $($response.message)" -ForegroundColor Gray
} catch {
    Write-Host "❌ Errore durante la raccolta: $($_.Exception.Message)" -ForegroundColor Red
    if ($backendProcess) {
        Stop-Process -Id $backendProcess.Id -Force -ErrorAction SilentlyContinue
    }
    exit 1
}

# Verifica articoli Google News
Write-Host "`nVerifica articoli da Google News..." -ForegroundColor Cyan

$jsonFile = "final_news_italian.json"
if (-not (Test-Path $jsonFile)) {
    $jsonFile = Join-Path ".." "backend" "final_news_italian.json"
}

if (Test-Path $jsonFile) {
    $data = Get-Content -Path $jsonFile -Raw | ConvertFrom-Json
    $totalArticles = $data.items.Count
    $googleNewsArticles = $data.items | Where-Object { 
        ($_.keywords -join " ").ToLower() -like "*google news*" -or 
        $_.author -like "*Google News*" 
    }
    
    Write-Host "   Totale articoli nel file: $totalArticles" -ForegroundColor White
    Write-Host "   Articoli da Google News: $($googleNewsArticles.Count)" -ForegroundColor $(if ($googleNewsArticles.Count -gt 0) { "Green" } else { "Yellow" })
    
    if ($googleNewsArticles.Count -gt 0) {
        Write-Host "`n✅ SUCCESSO! Articoli Google News trovati:" -ForegroundColor Green
        $googleNewsArticles | Select-Object -First 5 | ForEach-Object {
            Write-Host "   - $($_.title.Substring(0, [Math]::Min(70, $_.title.Length)))..." -ForegroundColor White
        }
    } else {
        Write-Host "`n⚠️  Nessun articolo Google News trovato nei keywords/author" -ForegroundColor Yellow
        Write-Host "   Verifica i log del backend per vedere se Google News è stato chiamato" -ForegroundColor Gray
    }
} else {
    Write-Host "⚠️  File JSON non trovato: $jsonFile" -ForegroundColor Yellow
}

# Pulisci: ferma il backend se l'abbiamo avviato noi
if ($backendProcess) {
    Write-Host "`nFermo il backend..." -ForegroundColor Yellow
    Stop-Process -Id $backendProcess.Id -Force -ErrorAction SilentlyContinue
    Write-Host "✅ Backend fermato" -ForegroundColor Green
}

Write-Host "`n✅ Test completato!" -ForegroundColor Green
Write-Host ""

