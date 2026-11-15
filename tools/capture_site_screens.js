#!/usr/bin/env node
const path = require('path');
const fs = require('fs');

// Use puppeteer from /tmp/node_modules if not local
let puppeteer;
try {
  puppeteer = require('puppeteer');
} catch (e) {
  puppeteer = require('/tmp/node_modules/puppeteer');
}

const ROOT = path.resolve(__dirname, '..');
const MEDIA_DIR = path.join(ROOT, 'docs', 'story', 'media');

if (!fs.existsSync(MEDIA_DIR)) {
  fs.mkdirSync(MEDIA_DIR, { recursive: true });
}

const targets = [
  {
    name: 'home',
    url: 'https://keremsumer2010-tech.github.io/aseltech/index.html',
    waitFor: 4000
  },
  {
    name: 'atlas',
    url: 'https://keremsumer2010-tech.github.io/aseltech/atlas.html',
    waitFor: 5000
  },
  {
    name: 'bulletin',
    url: 'https://keremsumer2010-tech.github.io/aseltech/docs/bulletins/eloy.html',
    waitFor: 3000
  },
  {
    name: 'game',
    url: 'https://keremsumer2010-tech.github.io/aseltech/game/index.html',
    waitFor: 4000
  }
];

const viewports = [
  { suffix: 'desk', width: 1440, height: 900, isMobile: false },
  { suffix: 'mob', width: 375, height: 812, isMobile: true }
];

async function main() {
  console.log('Launching headless Chrome via puppeteer...');
  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage']
  });

  const page = await browser.newPage();

  for (const t of targets) {
    for (const v of viewports) {
      const outName = `site_${t.name}_${v.suffix}.png`;
      const outPath = path.join(MEDIA_DIR, outName);

      console.log(`Setting viewport ${v.width}x${v.height} for ${t.name}...`);
      await page.setViewport({
        width: v.width,
        height: v.height,
        deviceScaleFactor: 2,
        isMobile: v.isMobile
      });

      console.log(`Navigating to ${t.url}...`);
      try {
        await page.goto(t.url, { waitUntil: 'networkidle2', timeout: 30000 });
      } catch (err) {
        console.warn(`Warning loading ${t.url}: ${err.message}, proceeding anyway`);
      }

      await new Promise(r => setTimeout(r, t.waitFor));

      console.log(`Capturing ${outPath}...`);
      await page.screenshot({ path: outPath, fullPage: false });
      const stat = fs.statSync(outPath);
      console.log(`Captured ${outName} (${(stat.size / 1024).toFixed(1)} KB)`);
    }
  }

  await browser.close();
  console.log('All 8 screenshots successfully captured.');
}

main().catch(err => {
  console.error('Fatal error during capture:', err);
  process.exit(1);
});
