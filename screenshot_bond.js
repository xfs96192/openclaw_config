const puppeteer = require('puppeteer-core');
const path = require('path');

(async () => {
  try {
    const browser = await puppeteer.launch({
      executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
      headless: 'new',
      args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    
    const page = await browser.newPage();
    await page.setViewport({ width: 1400, height: 900 });
    
    const htmlPath = 'file://' + path.resolve('/Users/fanshengxia/clawd/bond_chart.html');
    await page.goto(htmlPath, { waitUntil: 'networkidle0', timeout: 30000 });
    
    await new Promise(r => setTimeout(r, 3000));
    
    await page.screenshot({ 
      path: '/Users/fanshengxia/clawd/bond_chart.png', 
      fullPage: true 
    });
    
    await browser.close();
    console.log('Screenshot saved successfully');
  } catch (e) {
    console.error('Error:', e.message);
    process.exit(1);
  }
})();