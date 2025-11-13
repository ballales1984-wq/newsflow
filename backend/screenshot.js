// Script per fare screenshot del sito NewsFlow
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const siteUrl = 'https://newsflow-orcin.vercel.app';
const outputDir = path.join(__dirname, 'screenshots_sito');
const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);

// Crea cartella se non esiste
if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
}

(async () => {
    console.log('\n=== 📸 SCREENSHOT SITO NEWSFLOW ===\n');
    
    try {
        console.log('Avvio browser...');
        const browser = await chromium.launch({ headless: true });
        const page = await browser.newPage();
        
        // Imposta viewport
        await page.setViewportSize({ width: 1920, height: 1080 });
        
        console.log(`Caricamento sito: ${siteUrl}`);
        await page.goto(siteUrl, { waitUntil: 'networkidle', timeout: 30000 });
        
        // Attendi che il contenuto si carichi
        await page.waitForTimeout(3000);
        
        // Screenshot homepage
        const screenshotPath = path.join(outputDir, `homepage_${timestamp}.png`);
        await page.screenshot({ 
            path: screenshotPath, 
            fullPage: true 
        });
        console.log(`✅ Screenshot salvato: ${screenshotPath}`);
        
        // Screenshot viewport (solo schermo visibile)
        const viewportPath = path.join(outputDir, `viewport_${timestamp}.png`);
        await page.screenshot({ 
            path: viewportPath,
            fullPage: false
        });
        console.log(`✅ Screenshot viewport salvato: ${viewportPath}`);
        
        // Prova a navigare su una pagina articolo se disponibile
        try {
            const articleLink = await page.$('a[href*="/article/"]');
            if (articleLink) {
                await articleLink.click();
                await page.waitForTimeout(2000);
                
                const articlePath = path.join(outputDir, `article_${timestamp}.png`);
                await page.screenshot({ 
                    path: articlePath, 
                    fullPage: true 
                });
                console.log(`✅ Screenshot articolo salvato: ${articlePath}`);
            }
        } catch (e) {
            console.log('⚠️  Nessun articolo trovato per screenshot');
        }
        
        await browser.close();
        
        console.log('\n✅✅✅ SCREENSHOT COMPLETATI!');
        console.log(`\n📍 Screenshot salvati in: ${outputDir}\n`);
        
    } catch (error) {
        console.error('❌ Errore:', error.message);
        console.log('\n💡 Assicurati che Playwright sia installato:');
        console.log('   npm install playwright');
        console.log('   npx playwright install chromium\n');
        process.exit(1);
    }
})();

