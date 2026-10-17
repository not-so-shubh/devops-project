import test from 'node:test';
import assert from 'node:assert/strict';
import {stockStatus, csvCell, api} from './api.js';
test('threshold is inclusive and zero stock is distinct', () => {
  assert.equal(stockStatus({stock_quantity:0,reorder_threshold:0}),'out');
  assert.equal(stockStatus({stock_quantity:5,reorder_threshold:5}),'low');
  assert.equal(stockStatus({stock_quantity:6,reorder_threshold:5}),'healthy');
});
test('CSV escapes quotes and neutralizes formula input', () => {
  assert.equal(csvCell('a"b'), '"a""b"');
  assert.equal(csvCell('=CMD()'), '"\'=CMD()"');
});
test('API preserves server validation errors', async () => {
  const original = globalThis.fetch;
  globalThis.fetch = async () => ({ok:false,status:422,json:async()=>({detail:[{loc:['body','sku'],msg:'Invalid'}]})});
  try {await assert.rejects(()=>api('/products'), /sku: Invalid/);} finally {globalThis.fetch=original;}
});
test('API handles 204 deletes without attempting JSON', async () => {
  const original=globalThis.fetch;
  globalThis.fetch=async()=>({ok:true,status:204});
  try {assert.equal(await api('/products/1',{method:'DELETE'}),null);} finally {globalThis.fetch=original;}
});
