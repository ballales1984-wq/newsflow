# Script per aggiornamento automatico quotidiano delle notizie
# Esegue: raccolta -> aggiornamento file -> commit -> push -> aggiornamento PythonAnywhere

param(
    [switch]$SkipPush = $false,  # Salta push su GitHub se necessario
    [switch]$SkipPythonAnywhere = $false  # Salta aggiornamento PythonAnywhere
)

$ErrorActionPreference = "Stop"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Split-Path -Parent $scriptDir

Write-Host ""
Write-Host "="*70 -ForegroundColor Cyan
Write-Host "🔄 AGGIORNAMENTO AUTOMATICO NOTIZIE" -ForegroundColor Yellow
Write-Host "="*70 -ForegroundColor Cyan
Write-Host ""

# 1. Raccolta notizie
Write-Host "1️⃣  Raccolta notizie dai feed RSS..." -ForegroundColor Cyan
Set-Location $scriptDir
try {
    python collect_italian_priority.py
    if ($LASTEXITCODE -ne 0) {
        throw "Errore durante la raccolta notizie"
    }
    Write-Host "   ✅ Raccolta completata" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Errore: $_" -ForegroundColor Red
    exit 1
}

# 2. Aggiorna file final_news_italian.json
Write-Host ""
Write-Host "2️⃣  Aggiornamento file JSON..." -ForegroundColor Cyan
try {
    Copy-Item -Path "$scriptDir\italian_priority_news.json" -Destination "$scriptDir\final_news_italian.json" -Force
    Write-Host "   ✅ backend/final_news_italian.json aggiornato" -ForegroundColor Green
    
    # Aggiorna anche file frontend
    $frontendFile = Join-Path $projectRoot "frontend\src\assets\final_news_italian.json"
    Copy-Item -Path "$scriptDir\final_news_italian.json" -Destination $frontendFile -Force
    Write-Host "   ✅ frontend/src/assets/final_news_italian.json aggiornato" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Errore: $_" -ForegroundColor Red
    exit 1
}

# 3. Verifica statistiche
Write-Host ""
Write-Host "3️⃣  Verifica statistiche..." -ForegroundColor Cyan
try {
    $jsonContent = Get-Content "$scriptDir\final_news_italian.json" -Raw -Encoding UTF8 | ConvertFrom-Json
    $total = $jsonContent.items.Count
    $withImages = ($jsonContent.items | Where-Object { $_.image_url }).Count
    $percentage = [math]::Round(($withImages / $total) * 100, 1)
    
    Write-Host "   📊 Total articoli: $total" -ForegroundColor White
    Write-Host "   🖼️  Con immagini: $withImages ($percentage%)" -ForegroundColor White
    Write-Host "   ✅ Statistiche verificate" -ForegroundColor Green
} catch {
    Write-Host "   ⚠️  Impossibile verificare statistiche: $_" -ForegroundColor Yellow
}

# 4. Git commit e push
if (-not $SkipPush) {
    Write-Host ""
    Write-Host "4️⃣  Commit e push su GitHub..." -ForegroundColor Cyan
    Set-Location $projectRoot
    try {
        # Aggiungi file modificati
        git add backend/final_news_italian.json backend/italian_priority_news.json frontend/src/assets/final_news_italian.json
        
        # Commit con data/ora
        $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm"
        $commitMessage = "🔄 Aggiornamento notizie automatico - $timestamp"
        git commit -m $commitMessage
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "   ✅ Commit creato: $commitMessage" -ForegroundColor Green
            
            # Push
            git push origin main
            if ($LASTEXITCODE -eq 0) {
                Write-Host "   ✅ Push su GitHub completato" -ForegroundColor Green
            } else {
                Write-Host "   ⚠️  Errore durante push (potrebbe essere già aggiornato)" -ForegroundColor Yellow
            }
        } else {
            Write-Host "   ⚠️  Nessuna modifica da committare" -ForegroundColor Yellow
        }
    } catch {
        Write-Host "   ⚠️  Errore Git: $_" -ForegroundColor Yellow
        Write-Host "   💡 Verifica che Git sia configurato correttamente" -ForegroundColor Gray
    }
} else {
    Write-Host ""
    Write-Host "4️⃣  Push su GitHub saltato (--SkipPush)" -ForegroundColor Yellow
}

# 5. Aggiornamento PythonAnywhere
if (-not $SkipPythonAnywhere) {
    Write-Host ""
    Write-Host "5️⃣  Aggiornamento repository su PythonAnywhere..." -ForegroundColor Cyan
    try {
        # Configurazione PythonAnywhere
        $BASE_URL = 'https://www.pythonanywhere.com/api/v0/user/braccobaldo'
        $TOKEN = 'f17e14d4b1a12e0bf325cc0c1d8f9871fe50e599'
        $CONSOLE_ID = 43449916
        $HEADERS = @{
            'Authorization' = "Token $TOKEN"
        }
        
        # Invia comando git pull
        $body = @{
            input = "cd ~/newsflow`ngit pull`n"
        }
        
        $response = Invoke-RestMethod -Uri "$BASE_URL/consoles/$CONSOLE_ID/send_input/" `
            -Method Post `
            -Headers $HEADERS `
            -Body $body
        
        Write-Host "   ✅ Comando aggiornamento inviato a PythonAnywhere" -ForegroundColor Green
        Write-Host "   ⏳ L'aggiornamento verrà eseguito automaticamente" -ForegroundColor Yellow
    } catch {
        Write-Host "   ⚠️  Errore aggiornamento PythonAnywhere: $_" -ForegroundColor Yellow
        Write-Host "   💡 Puoi aggiornare manualmente: cd ~/newsflow && git pull" -ForegroundColor Gray
    }
} else {
    Write-Host ""
    Write-Host "5️⃣  Aggiornamento PythonAnywhere saltato (--SkipPythonAnywhere)" -ForegroundColor Yellow
}

# Riepilogo finale
Write-Host ""
Write-Host "="*70 -ForegroundColor Green
Write-Host "✅ AGGIORNAMENTO COMPLETATO!" -ForegroundColor Yellow
Write-Host "="*70 -ForegroundColor Green
Write-Host ""
Write-Host "📅 Data/Ora: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor White
Write-Host "🌐 Backend: https://braccobaldo.pythonanywhere.com/api/v1" -ForegroundColor Cyan
Write-Host "🌐 Frontend: https://newsflow-orcin.vercel.app" -ForegroundColor Cyan
Write-Host ""
Write-Host "💡 Per automatizzare:" -ForegroundColor Yellow
Write-Host "   • Task Scheduler Windows: esegui questo script ogni giorno" -ForegroundColor Gray
Write-Host "   • Oppure: esegui manualmente quando necessario" -ForegroundColor Gray
Write-Host ""

