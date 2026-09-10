(function (root, factory) {
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  else root.RevivalTracking = api;
})(typeof window !== 'undefined' ? window : globalThis, function () {
  'use strict';
  // Let GTM process a confirmed opt-in before navigation. Never block visitors
  // if GTM is slow, blocked, or has no matching tag. No contact details enter GTM.
  function confirmedOptIn(win, result) {
    if (result.preview) return Promise.resolve();
    return new Promise(resolve => {
      let complete = false;
      let timer;
      const finish = () => {
        if (complete) return;
        complete = true;
        win.clearTimeout(timer);
        resolve();
      };
      timer = win.setTimeout(finish, 1500);
      try {
        win.dataLayer = win.dataLayer || [];
        win.dataLayer.push({
          event: 'revival_optin_complete',
          campaign: 'revival',
          funnel_name: 'revival',
          revival_environment: 'production',
          eventCallback: finish,
          eventTimeout: 1400
        });
      } catch (_) { finish(); }
    });
  }
  return { confirmedOptIn };
});
