# Revival revision: RUK team handoff

Approval page: https://jmadops.github.io/ruk-revival-approval/review/

Landing page: https://jmadops.github.io/ruk-revival-approval/

## What this contains

A self-contained static landing page, a KSP-style opt-in modal, revised opt-in email copy, and the selected 10 original ads. The approval hub keeps the other 10 ads archived and labels the five scripts as saved for later, not reviewed for launch.

The page uses the existing Ministries Wistia video (`5w5ll9rwvc`), the original Our Approach background-image treatment, the supplied opening angle with Will's corrections, and the actual Ministries HTML/CSS section designs from Our Approach onward. Original backgrounds, glass cards, pillar layout, colors and Oswald/Inter typography are retained; this is no longer a re-templated lower page. Pricing, event dates, countdowns, and general Google star counts are omitted. The application is not embedded.

The page also includes three Google-review excerpts from Keith Cabral, Chris Rice and Mark Hernandez. Each review explicitly names Revival and has a direct Google review link. The ratings shown belong to those individual reviews. The existing pastor accounts and approved email copy remain unchanged by this addition. See `docs/review/downloads/google-reviews.md` for the source record.

## Reference funnels checked on 10 September 2026

All four repositories available in the Rise-Up-Kings organisation were inspected from current `main`:

| Repository | Funnel surfaces / relevance |
| --- | --- |
| `Rise-Up-Kings/ruk-virtual-paid-events` | Live KSP `/ksp`, A/B and waitlist variants, checkout and follow-up pages; MOS `/mos`. KSP's live CTA opens a required full-name/email/phone modal, posts a lead, then redirects. Its `vercel.json` maps `/ksp` to `kingdom-scaling-principles-embedded-lp/index.html`. This is the selected UI reference. |
| `Rise-Up-Kings/Ignite` | Data-driven city funnels and a shared name/email/phone waitlist dialog. Not the appropriate event-tagging destination for Revival. |
| `Rise-Up-Kings/2dayceo-web` | Free-book lead/checkout flow and marketing site; `/api/capture-lead` applies the `2dc-lead` tag. Do not reuse that campaign routing for Revival. |
| `Rise-Up-Kings/Documentary-Page` | Refinery documentary page linking into its own application flow. No equivalent native lead modal in the checked page. |

Reference code: https://github.com/Rise-Up-Kings/ruk-virtual-paid-events/blob/main/kingdom-scaling-principles-embedded-lp/index.html

Live KSP reference: https://live.riseupkings.com/ksp

## Current behaviour and the remaining connection

`docs/funnel-config.js` deliberately has `mode: 'preview'`. The form validates name, email and phone, then opens the confirmed `https://go.riseupkings.com/rukminapplication` application. Use sample details in this approval preview. It does not send requests, retain contact details, add them to URLs or fire a lead-conversion event. The modal clearly identifies the preview. The destination is the real application; completing it would submit a real application.

For the client PR, copy the self-contained landing-page bundle into the destination repo's correct public route. That repo/route has not been selected. Do not copy the approval hub into the prospect-facing route.

RUK's team must then configure:

1. `captureEndpoint`: a Revival-specific server endpoint using the team's existing GHL/contact integration.
2. `applicationUrl` is already confirmed and configured: `https://go.riseupkings.com/rukminapplication`.
3. `mode: 'live'` only after the endpoint, destination and consent wording are approved.
4. The team's approved privacy/terms links and any consent requirements for email/SMS. The current wording follows KSP's live modal. No SMS sequence is supplied or activated here.
5. The email application links are already populated. Add personalisation and the required sender/unsubscribe footer in the sending system.

Do not point this at KSP's production `/api/capture-lead`: that endpoint derives KSP event tags. Reuse the canonical contact helper in the destination repo and give Revival its own team-confirmed tags and lifecycle rules. Do not copy credentials into the static files.

## Capture contract

The frontend POSTs JSON with `name`, `email`, `phone`, `campaign: 'revival'`, `source: 'revival-landing'`, and an `attribution` object containing allowlisted UTM/click identifiers. Server-side validation and the destination repo's existing abuse protections must be applied before contact creation/upsert.

Return a successful HTTP response with `{ "ok": true }` only after the lead is accepted. Error, skipped, warning or failed responses remain on the form and offer a retry. The client times out after 12 seconds. This intentionally avoids inheriting KSP's fire-and-forget redirect, which could advance even when the lead was not saved. The capture endpoint should upsert contacts safely when a visitor retries.

After accepted capture, the page pushes `revival_optin_complete` to `dataLayer` without contact details, then redirects. Allowlisted campaign attribution follows the redirect; name, email and phone are not added to the URL. The team should map the event to its existing tracking tools once, and configure attribution storage on the server as required.

## Email lifecycle

Audience: people who opted in but have not submitted the application.

Timing: immediate, day 1, day 3, day 5, day 7. Every CTA continues the application. Stop this sequence when the application is received; the team must wire that event and handle qualified applicants in the appropriate later workflow. Booking links do not belong in this pre-application sequence.

E01 no longer assumes an application was completed. E04 uses the fuller verified Rob Satterfield excerpt. E02/E03/E05 retain their reviewed core copy, with only next-step and stage wording aligned to the opt-in-first flow. Primary ad copy remains the reviewed copy; ad-pair lists now reference A01–A10 only.

## Files and validation

- `docs/index.html`, `docs/landing.css`, `docs/ministries*.css`, `docs/ministries.js`, `docs/funnel*.js`, `docs/application-preview.html`, `docs/images/`, `docs/fonts/`: deployable page bundle.
- `docs/content/ministries.json`: source content and attribution.
- `docs/content/campaign-frame.html` and `docs/content/ministries-sections.html`: accepted campaign opening and retained source layouts.
- `source/ministries/`: original section snapshots and a record of limited changes.
- `scripts/build_landing.py`: regenerates the page from these templates and sourced reviews.
- `docs/review/content/emails.json`, `scripts/build_review.py`: approval-copy source and hub renderer.
- `scripts/package_campaign.py`: refreshes copy downloads and the campaign pack.
- `tests/funnel.test.cjs`: validation, preview isolation, capture contract, error and timeout checks. Uses mocked requests; no real leads submitted.

This revision is kept on `codex/revival-will-review` in Jay's approval repository. No Rise-Up-Kings repository has been modified and no client PR has been opened. Jay will choose the destination and open a single PR when ready. Client merges remain with RUK's team.
