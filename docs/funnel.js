(function () {
  'use strict';
  const dialog = document.getElementById('lead-modal');
  const form = document.getElementById('lead-form');
  if (!dialog || !form) return;
  const config = window.REVIVAL_FUNNEL || { mode: 'preview', previewUrl: 'application-preview.html' };
  const errorEl = document.getElementById('lead-error');
  const submit = form.querySelector('[type="submit"]');
  let opener;
  let busy = false;
  document.getElementById('preview-notice').hidden = config.mode !== 'preview';
  function close() { if (!busy) dialog.close(); }
  document.querySelectorAll('[data-apply]').forEach(button => {
    button.addEventListener('click', () => {
      opener = button;
      errorEl.hidden = true;
      dialog.showModal();
      document.body.classList.add('modal-open');
      document.getElementById('lead-name').focus();
    });
  });
  dialog.querySelector('.modal-close').addEventListener('click', close);
  dialog.addEventListener('click', event => {
    const box = dialog.getBoundingClientRect();
    if (event.target === dialog && (event.clientX < box.left || event.clientX > box.right || event.clientY < box.top || event.clientY > box.bottom)) close();
  });
  dialog.addEventListener('cancel', event => { if (busy) event.preventDefault(); });
  dialog.addEventListener('close', () => {
    document.body.classList.remove('modal-open');
    if (opener) opener.focus();
  });
  form.addEventListener('input', () => { errorEl.hidden = true; });
  form.addEventListener('submit', async event => {
    event.preventDefault();
    if (busy) return;
    const input = Object.fromEntries(new FormData(form));
    const validation = window.RevivalFunnelCore.validateLead(input);
    if (validation.error) {
      errorEl.textContent = validation.error; errorEl.hidden = false;
      form.elements[validation.field].focus(); return;
    }
    busy = true; submit.disabled = true; form.setAttribute('aria-busy', 'true'); errorEl.hidden = true;
    const buttonHtml = submit.innerHTML;
    submit.textContent = 'Continuing…';
    try {
      const result = await window.RevivalFunnelCore.submitLead(config, input, { baseUrl: location.href, fetchImpl: window.fetch.bind(window) });
      if (!result.preview) {
        window.dataLayer = window.dataLayer || [];
        window.dataLayer.push({ event: 'revival_optin_complete', campaign: 'revival' });
      }
      form.reset();
      window.location.assign(result.nextUrl);
    } catch (error) {
      errorEl.textContent = error.message || 'Something went wrong. Please try again.';
      errorEl.hidden = false;
    } finally {
      busy = false; submit.disabled = false; submit.innerHTML = buttonHtml; form.removeAttribute('aria-busy');
    }
  });
})();
