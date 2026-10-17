import {chromium} from '../e2e/node_modules/@playwright/test/index.mjs';
import {execFileSync} from 'node:child_process';
const browser=await chromium.launch({headless:true});
const page=await browser.newPage({viewport:{width:1440,height:1000}});
try {
  await page.goto('http://localhost:9090/targets');
  await page.waitForTimeout(3000);
  await page.evaluate(() => {
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    let node;
    while ((node = walker.nextNode())) node.textContent = node.textContent.replace(/\b10(?:\.\d{1,3}){3}\b/g, '[cluster address redacted]');
  });
  await page.screenshot({path:'../docs/evidence/prometheus-targets.png',fullPage:true});
  const password=execFileSync('kubectl',['get','secret','stockpilot-grafana','-n','monitoring','-o','jsonpath={.data.admin-password}'],{encoding:'utf8'});
  await page.goto('http://localhost:3001/login');
  await page.getByLabel(/email or username/i).fill('admin');
  await page.locator('input[name="password"]').fill(Buffer.from(password,'base64').toString());
  const loginResponse = page.waitForResponse(response => new URL(response.url()).pathname === '/login' && response.request().method() === 'POST');
  await page.getByRole('button',{name:/log in/i}).click();
  const authenticated = await loginResponse;
  if (!authenticated.ok()) throw new Error(`Grafana login returned HTTP ${authenticated.status()}`);
  await page.waitForURL(url => !url.pathname.startsWith('/login'), {timeout:30000});
  await page.goto('http://localhost:3001/d/stockpilot-ops/stockpilot-operations?from=now-15m&to=now');
  await page.getByText('Request rate',{exact:true}).first().waitFor({timeout:30000});
  await page.waitForTimeout(10000);
  await page.screenshot({path:'../docs/evidence/grafana-dashboard.png',fullPage:true});
} catch (error) {
  console.error('Grafana capture failed at path:', new URL(page.url()).pathname, 'page:', await page.title());
  await page.screenshot({path:'../docs/evidence/grafana-failure.png',fullPage:true,mask:[page.locator('input[type="password"]')]});
  throw error;
} finally {await browser.close();}
