/* Approval preview. RUK's team sets the production endpoint and destinations before launch.
 * Never use KSP's capture endpoint unchanged: it applies KSP event tags. See HANDOFF.md.
 */
window.REVIVAL_FUNNEL = Object.freeze({
  mode: 'preview',
  captureEndpoint: '',
  applicationUrl: '',
  previewUrl: 'application-preview.html',
  source: 'revival-landing',
  timeoutMs: 12000
});
