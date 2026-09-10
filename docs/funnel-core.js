(function (root, factory) {
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  else root.RevivalFunnelCore = api;
})(typeof window !== 'undefined' ? window : globalThis, function () {
  'use strict';
  const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[A-Za-z]{2,}$/;
  function validateLead(input) {
    const lead = Object.fromEntries(['name', 'email', 'phone'].map(key => [key, String(input[key] || '').trim()]));
    for (const field of ['name', 'email', 'phone']) {
      if (!lead[field]) return { error: 'Please enter your ' + (field === 'name' ? 'full name' : field === 'email' ? 'email address' : 'phone number') + '.', field };
    }
    if (!EMAIL_RE.test(lead.email) || lead.email.length > 254) return { error: 'Please enter a valid email address, such as you@example.com.', field: 'email' };
    if (lead.name.length > 120) return { error: 'Please shorten your name to 120 characters or fewer.', field: 'name' };
    const digits = lead.phone.replace(/\D/g, '');
    if (digits.length < 7 || digits.length > 15 || !/^[+\d\s().-]+$/.test(lead.phone) || lead.phone.length > 30) return { error: 'Please enter a valid phone number, including your area or country code.', field: 'phone' };
    return { lead };
  }
  function resolveUrl(value, base) {
    if (typeof value !== 'string' || !value.trim()) throw new Error('The application flow is not connected yet. Please try again later.');
    const url = new URL(value, base);
    if (!['https:', 'http:'].includes(url.protocol) || url.username || url.password) throw new Error('The application destination is not configured correctly.');
    if (url.protocol === 'http:' && !['localhost', '127.0.0.1'].includes(url.hostname)) throw new Error('The application destination requires a secure connection.');
    return url;
  }
  function campaignParams(base) {
    const params = new URL(base).searchParams;
    return Object.fromEntries(['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term', 'gclid', 'fbclid'].filter(k => params.has(k)).map(k => [k, params.get(k).slice(0, 500)]));
  }
  async function submitLead(config, input, deps) {
    const validation = validateLead(input);
    if (validation.error) return validation;
    const { baseUrl, fetchImpl } = deps;
    if (config.mode === 'preview') {
      // No requests, storage, contact data in the URL, or real conversion events.
      return { preview: true, nextUrl: resolveUrl(config.applicationUrl || config.previewUrl, baseUrl).href };
    }
    if (config.mode !== 'live') throw new Error('The application flow is not connected yet. Please try again later.');
    const endpoint = resolveUrl(config.captureEndpoint, baseUrl);
    const next = resolveUrl(config.applicationUrl, baseUrl);
    const campaign = campaignParams(baseUrl);
    for (const [key, value] of Object.entries(campaign)) next.searchParams.set(key, value);
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), config.timeoutMs || 12000);
    try {
      const response = await fetchImpl(endpoint.href, {
        method: 'POST', headers: { 'Content-Type': 'application/json' }, signal: controller.signal,
        body: JSON.stringify({ ...validation.lead, campaign: 'revival', source: config.source || 'revival-landing', attribution: campaign })
      });
      if (!response.ok) throw new Error('We couldn’t save your details. Please try again.');
      const receipt = await response.json();
      if (!receipt || receipt.ok !== true || receipt.skipped || receipt.warning || ['skipped', 'failed'].includes(receipt.ghl)) throw new Error('We couldn’t confirm your details were received. Please try again.');
      return { preview: false, nextUrl: next.href };
    } catch (error) {
      if (error.name === 'AbortError') throw new Error('That took too long. Please try again.');
      throw error;
    } finally { clearTimeout(timeout); }
  }
  return { validateLead, resolveUrl, campaignParams, submitLead };
});
