const { test } = require('node:test');
const assert = require('node:assert/strict');
const { confirmedOptIn } = require('../docs/tracking.js');
function harness() {
 const timers = new Map(); let sequence = 0;
 return { dataLayer: [], timers,
  setTimeout(fn) { const id = ++sequence; timers.set(id, fn); return id; },
  clearTimeout(id) { timers.delete(id); }
 };
}
test('approval previews emit no lead conversion and do not delay navigation', async () => {
 const win = harness(); await confirmedOptIn(win, { preview: true });
 assert.deepEqual(win.dataLayer, []); assert.equal(win.timers.size, 0);
});
test('confirmed capture waits for GTM without sharing contact details', async () => {
 const win = harness(); let resolved = false;
 const done = confirmedOptIn(win, { preview: false, nextUrl: 'https://example.org' }).then(() => { resolved = true; });
 await Promise.resolve(); assert.equal(resolved, false);
 const event = win.dataLayer[0];
 assert.equal(event.event, 'revival_optin_complete');
 assert.equal(event.revival_environment, 'production');
 assert.deepEqual(Object.keys(event).sort(), ['event','campaign','funnel_name','revival_environment','eventCallback','eventTimeout'].sort());
 event.eventCallback(); event.eventCallback(); await done;
 assert.equal(resolved, true); assert.equal(win.timers.size, 0); assert.equal(win.dataLayer.length, 1);
});
test('blocked GTM cannot prevent redirect, and a late callback is harmless', async () => {
 const win = harness(); const done = confirmedOptIn(win, { preview: false });
 const fallback = [...win.timers.values()][0]; fallback(); await done;
 win.dataLayer[0].eventCallback(); assert.equal(win.timers.size, 0);
});
test('a failing tracking library cannot prevent redirect after successful capture', async () => {
 const win = harness(); win.dataLayer.push = () => { throw new Error('blocked'); };
 await confirmedOptIn(win, { preview: false }); assert.equal(win.timers.size, 0);
});
