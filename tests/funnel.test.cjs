const { test } = require('node:test');
const assert = require('node:assert/strict');
const { validateLead, submitLead } = require('../docs/funnel-core.js');
const lead = { name: 'Example Pastor', email: 'example@example.org', phone: '+1 555 010 1234' };
const baseUrl = 'https://example.org/revival/?utm_source=review&utm_campaign=revival&email=should-not-pass@example.org';
const config = { mode: 'live', captureEndpoint: '/api/revival-lead', applicationUrl: '/application', source: 'revival-landing' };
test('published configuration previews the confirmed application without capturing a lead', async () => {
 const fs = require('node:fs');
 const vm = require('node:vm');
 const context = { window: {} };
 vm.runInNewContext(fs.readFileSync(require.resolve('../docs/funnel-config.js'), 'utf8'), context);
 const published = context.window.REVIVAL_FUNNEL;
 assert.equal(published.mode, 'preview');
 const result = await submitLead(published, lead, { baseUrl, fetchImpl: () => assert.fail('preview must never save a lead') });
 assert.equal(result.nextUrl, 'https://go.riseupkings.com/rukminapplication');
 assert.equal(result.preview, true);
 const live = await submitLead({ ...published, mode: 'live', captureEndpoint: '/api/revival-lead' }, lead, {
  baseUrl, fetchImpl: async () => ({ ok: true, json: async () => ({ ok: true }) })
 });
 assert.equal(live.nextUrl, 'https://go.riseupkings.com/rukminapplication?utm_source=review&utm_campaign=revival');
});
test('preview validates but never sends or propagates contact details', async () => {
 let calls = 0;
 const result = await submitLead({ mode: 'preview', previewUrl: 'application-preview.html' }, lead, { baseUrl, fetchImpl: () => { calls++; } });
 assert.equal(calls, 0); assert.equal(result.preview, true);
 assert.equal(result.nextUrl, 'https://example.org/revival/application-preview.html');
});
test('missing and invalid fields prevent capture', async () => {
 for (const input of [{ ...lead, name: ' ' }, { ...lead, email: 'a@b' }, { ...lead, phone: '123' }, { ...lead, phone: 'abcdefghijk' }]) {
  assert.ok(validateLead(input).error);
  const result = await submitLead(config, input, { baseUrl, fetchImpl: () => assert.fail('must not send') });
  assert.ok(result.error);
 }
});
test('live mode requires both destinations before sending', async () => {
 for (const change of [{ captureEndpoint: '' }, { applicationUrl: '' }, { applicationUrl: 'javascript:alert(1)' }, { mode: 'unknown' }]) {
  await assert.rejects(submitLead({ ...config, ...change }, lead, { baseUrl, fetchImpl: () => assert.fail('must not send') }));
 }
});
test('capture receives Revival data, then passes only campaign attribution to application', async () => {
 let request;
 const result = await submitLead(config, lead, { baseUrl, fetchImpl: async (url, options) => {
  request = { url, ...options }; return { ok: true, json: async () => ({ ok: true }) };
 } });
 assert.equal(request.url, 'https://example.org/api/revival-lead'); assert.equal(request.method, 'POST');
 const payload = JSON.parse(request.body);
 assert.equal(payload.campaign, 'revival'); assert.equal(payload.email, lead.email);
 assert.equal(payload.attribution.utm_campaign, 'revival'); assert.equal(payload.attribution.email, undefined);
 assert.equal(result.nextUrl, 'https://example.org/application?utm_source=review&utm_campaign=revival');
 assert.equal(result.preview, false);
});
test('failed, skipped, ambiguous or unreachable capture does not advance', async () => {
 const responses = [
  { ok: false },
  ...[{ ok: false }, { ok: true, skipped: true }, { ok: true, warning: 'ghl_unreachable' }, { ok: true, ghl: 'failed' }, { ok: true, ghl: 'skipped' }, {}].map(body => ({ ok: true, json: async () => body }))
 ];
 for (const response of responses) await assert.rejects(submitLead(config, lead, { baseUrl, fetchImpl: async () => response }));
 await assert.rejects(submitLead(config, lead, { baseUrl, fetchImpl: async () => { throw new Error('Network error'); } }));
});
test('timeout reports retry rather than advancing', async () => {
 await assert.rejects(submitLead({ ...config, timeoutMs: 5 }, lead, { baseUrl, fetchImpl: (url, { signal }) => new Promise((resolve, reject) => signal.addEventListener('abort', () => reject(Object.assign(new Error('timeout'), { name: 'AbortError' })))) }), /too long/);
});
