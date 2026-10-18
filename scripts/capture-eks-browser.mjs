import {chromium, expect} from '../e2e/node_modules/@playwright/test/index.mjs';
import {readFileSync, writeFileSync} from 'node:fs';

const credentials = JSON.parse(readFileSync(0, 'utf8'));
const browser = await chromium.launch({headless:true});
const context = await browser.newContext({viewport:{width:1440,height:1100}});
const page = await context.newPage();
page.setDefaultTimeout(30000);
const summary = {
  environment:'real AWS EKS, ap-southeast-2',
  application_source_sha:process.env.APP_SOURCE_SHA,
  captured_at:new Date().toISOString(),
  kind_cluster:false
};
try {
  const targetsResponse = await context.request.get('http://127.0.0.1:9090/api/v1/targets');
  expect(targetsResponse.ok()).toBeTruthy();
  const targets = await targetsResponse.json();
  const applicationTargets = targets.data.activeTargets.filter(t => t.labels?.namespace === 'stockpilot');
  expect(applicationTargets.length).toBeGreaterThanOrEqual(2);
  expect(applicationTargets.every(t => t.health === 'up')).toBeTruthy();
  summary.prometheus_targets_up = applicationTargets.length;
  await page.goto('http://127.0.0.1:9090/targets');
  await expect(page.getByText(/stockpilot/i).first()).toBeVisible();
  await page.screenshot({path:'../docs/evidence/eks-prometheus-targets.png',fullPage:true});
  await page.goto('http://127.0.0.1:3001/login');
  await page.getByLabel(/email or username/i).fill(credentials.username);
  await page.locator('input[name="password"]').fill(credentials.password);
  const login = page.waitForResponse(response =>
    new URL(response.url()).pathname === '/login' && response.request().method() === 'POST');
  await page.getByRole('button',{name:/log in/i}).click();
  expect((await login).ok()).toBeTruthy();
  await page.waitForURL(url => !url.pathname.startsWith('/login'));
  const dataResponse = page.waitForResponse(response =>
    new URL(response.url()).pathname === '/api/ds/query' &&
    response.request().method() === 'POST' && response.ok());
  await page.goto('http://127.0.0.1:3001/d/stockpilot-ops/stockpilot-operations?from=now-15m&to=now');
  await expect(page.getByText('Request rate',{exact:true}).first()).toBeVisible();
  const data = await (await dataResponse).json();
  const populated = Object.values(data.results || {}).some(result =>
    (result.frames || []).some(frame =>
      (frame.data?.values?.slice(1) || []).some(values =>
        values.some(value => typeof value === 'number' && Number.isFinite(value)))));
  expect(populated).toBeTruthy();
  await expect(page.getByText('Backend targets up',{exact:true}).first()).toBeVisible();
  await page.screenshot({path:'../docs/evidence/eks-grafana-dashboard.png',fullPage:true});
  summary.grafana_authenticated = true;
  summary.grafana_query_has_numeric_data = true;
  const metricResponse = await context.request.get('http://127.0.0.1:9090/api/v1/query', {
    params:{query:'sum(rate(stockpilot_http_requests_total{namespace="stockpilot"}[2m]))'}
  });
  const metricData = await metricResponse.json();
  const rate = Number(metricData.data.result[0]?.value[1]);
  expect(Number.isFinite(rate) && rate > 0).toBeTruthy();
  summary.request_rate_per_second = rate;
  writeFileSync('../docs/evidence/eks-browser-summary.json', JSON.stringify(summary,null,2)+'\n');
  console.log('PASS: real EKS Prometheus targets and authenticated Grafana with live data captured');
} finally {
  await context.close();
  await browser.close();
}
