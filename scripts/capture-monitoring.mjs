import {chromium} from '../e2e/node_modules/@playwright/test/index.mjs';
import {execFileSync} from 'node:child_process';
const browser=await chromium.launch({headless:true});
try {
  const page=await browser.newPage({viewport:{width:1440,height:1000}});
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
  await page.getByLabel(/password/i,{exact:true}).fill(Buffer.from(password,'base64').toString());
  await page.getByRole('button',{name:/log in/i}).click();
  await page.goto('http://localhost:3001/d/stockpilot-ops/stockpilot-operations?from=now-15m&to=now');
  await page.getByText('Request rate',{exact:true}).first().waitFor({timeout:30000});
  await page.waitForTimeout(10000);
  await page.screenshot({path:'../docs/evidence/grafana-dashboard.png',fullPage:true});
} finally {await browser.close();}
