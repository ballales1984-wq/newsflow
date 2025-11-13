// Script per fare screenshot della nuova home page NewsFlow
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

// URL del sito (usa quello locale se disponibile, altrimenti Vercel)
const siteUrl = process.env.SITE_URL || 'https://newsflow-orcin.vercel.app';
const outputDir = path.join(__dirname, 'screenshots_sito');
const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);

// Crea cartella se non esiste
if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
}

(async () => {
    console.log('\n=== 📸 SCREENSHOT HOME PAGE NEWSFLOW ===\n');
    
    try {
        console.log('Avvio browser...');
        const browser = await chromium.launch({ headless: true });
        
        // SCREENSHOT 1: Desktop (1920x1080)
        console.log('\n📸 Screenshot 1: Desktop (1920x1080)...');
        const pageDesktop = await browser.newPage();
        await pageDesktop.setViewportSize({ width: 1920, height: 1080 });
        
        console.log(`Caricamento sito: ${siteUrl}`);
        await pageDesktop.goto(siteUrl, { waitUntil: 'networkidle', timeout: 30000 });
        
        // Attendi che il contenuto si carichi completamente
        await pageDesktop.waitForTimeout(5000);
        
        // Scroll fino in fondo per caricare tutti gli articoli
        await pageDesktop.evaluate(() => {
            return new Promise((resolve) => {
                let totalHeight = 0;
                const distance = 100;
                const timer = setInterval(() => {
                    const scrollHeight = document.body.scrollHeight;
                    window.scrollBy(0, distance);
                    totalHeight += distance;
                    
                    if(totalHeight >= scrollHeight){
                        clearInterval(timer);
                        resolve();
                    }
                }, 100);
            });
        });
        
        // Torna in alto
        await pageDesktop.evaluate(() => window.scrollTo(0, 0));
        await pageDesktop.waitForTimeout(1000);
        
        const screenshotDesktop = path.join(outputDir, `homepage_desktop_${timestamp}.png`);
        await pageDesktop.screenshot({ 
            path: screenshotDesktop, 
            fullPage: true 
        });
        console.log(`✅ Screenshot desktop salvato: ${screenshotDesktop}`);
        
        await pageDesktop.close();
        
        // SCREENSHOT 2: Mobile (375x667 - iPhone)
        console.log('\n📸 Screenshot 2: Mobile (375x667)...');
        const pageMobile = await browser.newPage();
        await pageMobile.setViewportSize({ width: 375, height: 667 });
        
        console.log(`Caricamento sito mobile: ${siteUrl}`);
        await pageMobile.goto(siteUrl, { waitUntil: 'networkidle', timeout: 30000 });
        
        // Attendi che il contenuto si carichi completamente
        await pageMobile.waitForTimeout(5000);
        
        // Scroll fino in fondo per caricare tutti gli articoli
        await pageMobile.evaluate(() => {
            return new Promise((resolve) => {
                let totalHeight = 0;
                const distance = 100;
                const timer = setInterval(() => {
                    const scrollHeight = document.body.scrollHeight;
                    window.scrollBy(0, distance);
                    totalHeight += distance;
                    
                    if(totalHeight >= scrollHeight){
                        clearInterval(timer);
                        resolve();
                    }
                }, 100);
            });
        });
        
        // Torna in alto
        await pageMobile.evaluate(() => window.scrollTo(0, 0));
        await pageMobile.waitForTimeout(1000);
        
        const screenshotMobile = path.join(outputDir, `homepage_mobile_${timestamp}.png`);
        await pageMobile.screenshot({ 
            path: screenshotMobile, 
            fullPage: true 
        });
        console.log(`✅ Screenshot mobile salvato: ${screenshotMobile}`);
        
        await pageMobile.close();
        await browser.close();
        
        console.log('\n✅✅✅ SCREENSHOT COMPLETATI!');
        console.log(`\n📍 Screenshot salvati in: ${outputDir}`);
        console.log(`   - Desktop: homepage_desktop_${timestamp}.png`);
        console.log(`   - Mobile: homepage_mobile_${timestamp}.png\n`);
        
    } catch (error) {
        console.error('❌ Errore:', error.message);
        console.log('\n💡 Assicurati che Playwright sia installato:');
        console.log('   cd backend');
        console.log('   npm install playwright');
        console.log('   npx playwright install chromium\n');
        process.exit(1);
    }
})();

