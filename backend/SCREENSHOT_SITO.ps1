# Script per fare screenshot del sito NewsFlow
# Richiede: Chrome/Edge installato

$siteUrl = "https://newsflow-orcin.vercel.app"
$outputDir = "$PSScriptRoot\screenshots_sito"
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"

# Crea cartella screenshots se non esiste
if (-not (Test-Path $outputDir)) {
    New-Item -ItemType Directory -Path $outputDir -Force | Out-Null
}

Write-Host "`n=== 📸 SCREENSHOT SITO NEWSFLOW ===" -ForegroundColor Cyan
Write-Host ""

# Prova con Chrome/Chromium
$chromePaths = @(
    "${env:ProgramFiles}\Google\Chrome\Application\chrome.exe",
    "${env:ProgramFiles(x86)}\Google\Chrome\Application\chrome.exe",
    "${env:LOCALAPPDATA}\Google\Chrome\Application\chrome.exe",
    "${env:ProgramFiles}\Microsoft\Edge\Application\msedge.exe",
    "${env:ProgramFiles(x86)}\Microsoft\Edge\Application\msedge.exe"
)

$browserPath = $null
foreach ($path in $chromePaths) {
    if (Test-Path $path) {
        $browserPath = $path
        break
    }
}

if (-not $browserPath) {
    Write-Host "❌ Chrome/Edge non trovato!" -ForegroundColor Red
    Write-Host "   Apri manualmente il sito e fai screenshot" -ForegroundColor Yellow
    Start-Process $siteUrl
    exit 1
}

Write-Host "Browser trovato: $browserPath" -ForegroundColor Green
Write-Host ""

# Usa Playwright se disponibile, altrimenti apre browser
try {
    # Prova con Playwright
    $playwrightInstalled = Get-Command playwright -ErrorAction SilentlyContinue
    if ($playwrightInstalled) {
        Write-Host "Usando Playwright per screenshot..." -ForegroundColor Yellow
        playwright screenshot --full-page "$siteUrl" "$outputDir\sito_$timestamp.png"
        Write-Host "✅ Screenshot salvato!" -ForegroundColor Green
    } else {
        throw "Playwright non disponibile"
    }
} catch {
    # Metodo alternativo: usa Selenium o apre browser manualmente
    Write-Host "⚠️  Playwright non disponibile" -ForegroundColor Yellow
    Write-Host "   Apertura browser per screenshot manuale..." -ForegroundColor Yellow
    
    # Apri il sito
    Start-Process $browserPath -ArgumentList "--new-window", $siteUrl
    
    Write-Host ""
    Write-Host "📸 ISTRUZIONI:" -ForegroundColor Cyan
    Write-Host "   1. Attendi che il sito si carichi completamente" -ForegroundColor White
    Write-Host "   2. Premi Windows + Stamp (o Fn + Stamp)" -ForegroundColor White
    Write-Host "   3. Oppure usa Snipping Tool (Windows + Shift + S)" -ForegroundColor White
    Write-Host "   4. Salva nella cartella: $outputDir" -ForegroundColor White
    Write-Host ""
    Write-Host "   Oppure installa Playwright:" -ForegroundColor Yellow
    Write-Host "   npm install -g playwright" -ForegroundColor Gray
    Write-Host "   playwright install chromium" -ForegroundColor Gray
}

Write-Host ""
Write-Host "📍 Screenshot salvati in: $outputDir" -ForegroundColor Cyan
Write-Host ""

