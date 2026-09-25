// Verificación con Chrome real: capturas por sección (desktop + mobile), overflow y flujo de reservas.
// Uso: node verify.cjs [url]
const { chromium } = require('C:/Users/santi/Desktop/Claude Code/pueyrredon-lavadero/node_modules/playwright');
const URL = process.argv[2] || 'http://localhost:8851/';
const OUT = process.env.OUT || 'C:/Users/santi/AppData/Local/Temp/ce-shots';
require('fs').mkdirSync(OUT, { recursive: true });

(async () => {
  const browser = await chromium.launch({ channel: 'chrome' });
  for (const vp of [{ name: 'desk', width: 1440, height: 900 }, { name: 'mob', width: 375, height: 812, isMobile: true }]) {
    const ctx = await browser.newContext({ viewport: { width: vp.width, height: vp.height }, isMobile: !!vp.isMobile, hasTouch: !!vp.isMobile, deviceScaleFactor: 1 });
    const page = await ctx.newPage();
    const errors = [];
    page.on('pageerror', e => errors.push(e.message));
    page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
    await page.goto(URL, { waitUntil: 'networkidle' });
    await page.addStyleTag({ content: 'html{scroll-behavior:auto!important}' });
    const shot = async (n) => page.screenshot({ path: `${OUT}/${vp.name}-${n}.png` });
    await page.waitForTimeout(3400); await shot('00-hero');
    for (const p of [0.02, 0.24, 0.46, 0.7, 0.95]) {
      await page.evaluate(p => { const s = document.getElementById('tropico'); scrollTo(0, s.offsetTop + (s.offsetHeight - innerHeight) * p); }, p);
      await page.waitForTimeout(600); await shot('01-reloj-' + p);
    }
    const sections = ['#cabanas', '#adentro-t', '#voces-t', '#mesa-t', '#vid-t', '#gal-t', '#quebrada', '#promo-t', '#reservar', '#llegar', '#faq-t', '#cierre-t'];
    let i = 2;
    for (const sel of sections) {
      await page.evaluate(sel => { const e = document.querySelector(sel); scrollTo(0, e.getBoundingClientRect().top + scrollY - 80); }, sel);
      await page.waitForTimeout(900); await shot(String(i++).padStart(2, '0') + '-' + sel.replace(/\W/g, ''));
      if (vp.name === 'mob' || sel === '#cabanas' || sel === '#gal-t' || sel === '#mesa-t') { await page.evaluate(() => scrollBy(0, innerHeight * .75)); await page.waitForTimeout(800); await shot(String(i - 1).padStart(2, '0') + '-' + sel.replace(/\W/g, '') + '-b'); }
    }
    // flujo de reservas completo
    await page.evaluate(() => { const e = document.getElementById('bkw-root'); scrollTo(0, e.getBoundingClientRect().top + scrollY - 100); });
    await page.selectOption('#bkw-pax', '4');
    await page.click('#bkw-search'); await page.waitForTimeout(900); await shot('20-res-results');
    await page.click('#bkw-step-results button[data-name]'); await page.waitForTimeout(300);
    await page.fill('#bkw-name', 'Prueba Demo'); await shot('21-res-form');
    await page.click('#bkw-confirm'); await page.waitForTimeout(1000); await shot('22-res-done');
    const wa = await page.getAttribute('#bkw-step-done a.btn-wa', 'href');
    // FAQ + lightbox
    await page.click('.acc-trigger'); await page.waitForTimeout(500);
    const overflow = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
    if (vp.name === 'mob') { await page.evaluate(() => scrollTo(0, 0)); await page.click('#burger'); await page.waitForTimeout(400); await shot('30-menu'); await page.click('#burger'); }
    await page.evaluate(() => document.querySelector('#gal button').scrollIntoView()); await page.click('#gal button'); await page.waitForTimeout(500); await shot('31-lightbox'); for (let t = 0; t < 5; t++) await page.keyboard.press('Tab'); const trapped = await page.evaluate(() => document.getElementById('lb').contains(document.activeElement)); await page.keyboard.press('Escape');
    await page.evaluate(() => document.querySelector('#vids').scrollIntoView()); await page.click('.vid-play'); await page.waitForTimeout(2500); const playing = await page.evaluate(() => { const v = document.querySelector('.vid video'); return v && !v.paused && v.currentTime > 0; }); await shot('32-video');
    console.log(vp.name, { overflow, wa, trapped, playing, errors });
    await ctx.close();
  }
  await browser.close();
})();
