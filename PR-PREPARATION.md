# Revival landing page — prepared change, no PR opened

## Proposed PR title

Add Revival campaign landing page with opt-in flow and RUK tracking

## Proposed description

Adds the Revival campaign opening and Ministries video above the existing Ministries section layouts. Background photography remains behind its original content, with the source cards, four pillars, typography and FAQ styling retained. Pricing and event dates remain omitted. The page includes sourced Revival review excerpts and keeps the application as a separate page.

Apply opens the name/email/phone opt-in. After accepted lead capture, visitors continue to https://go.riseupkings.com/rukminapplication. GTM-WJW6VTZ loads on the landing page; a confirmed opt-in emits revival_optin_complete before navigation, with a fallback if tracking is unavailable. Preview mode does not save contacts or emit that conversion.

Validation covers form errors, rejected/skipped capture, timeouts, the confirmed application URL, tracking callbacks and blocked tracking. No real contacts or applications were submitted. The selected ads are unchanged; the five opt-in emails now use the confirmed application URL.

## Integration status

- Landing page, original section styles, local assets, application destination and GTM installation: prepared.
- Approval mode: enabled intentionally in funnel-config.js.
- Target client repository and final public route: to be confirmed before the PR is prepared against client main.
- Revival-specific capture endpoint and GHL campaign tags/workflow: still needed. Do not use KSP’s endpoint unchanged.
- GTM custom-event mapping: tracking owner must confirm revival_optin_complete triggers the intended conversion tags and excludes approval traffic.
- Email sender details, unsubscribe footer and application-submitted suppression: configured in RUK’s sending system before activation.

## Deployment files

Copy only the Landing Page folder from the campaign pack to the chosen public route. It includes index.html, landing.css, ministries.css, ministries-integration.css, ministries.js, tracking.js, funnel-config.js, funnel-core.js, funnel.js, application-preview.html, images, fonts and content. The approval hub, ads and email review pages are review materials, not part of the prospect route.

Before opening the PR, branch from current client main, integrate a Revival-specific server endpoint using that repository’s canonical contact helper, and run its required checks. Set captureEndpoint and mode: live only once the endpoint and tagging are ready. Preserve the source’s canonical owner for consent and analytics; do not duplicate the GTM container if the destination layout already includes it.

No PR has been opened. No client main branch has been changed.
