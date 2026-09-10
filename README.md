# Revival campaign approval

Approval hub: https://jmadops.github.io/ruk-revival-approval/review/

Landing page: https://jmadops.github.io/ruk-revival-approval/

Updated from Will's feedback on 10 September 2026. GitHub Pages serves `docs/` from `main`.

## Included

- A revised price-free, date-free landing page with the existing Ministries video and original section layouts from Our Approach onward.
- A full-name/email/phone opt-in modal based on the live KSP funnel.
- Preview mode: no lead collection or contact storage; the confirmed application opens after sample details; the production capture endpoint remains pending.
- Five emails for opt-ins who have not submitted an application.
- Ten selected original ads, with ten earlier variations archived.
- Three primary-copy options and five scripts saved for later.
- Source notes, full client download pack and a client-team handoff.

Read [HANDOFF.md](HANDOFF.md) for the four client repositories checked, the form contract, outstanding connection points and the client PR scope. No RUK client repository has been modified.

## Updates

- Landing page: edit `docs/content/campaign-frame.html`, `docs/content/ministries-sections.html`, `docs/content/ministries.json` and their CSS. Preserve the original source styles recorded in `source/ministries/`;; run `python3 scripts/build_landing.py`.
- Form: `docs/funnel-config.js`, `docs/funnel-core.js`, `docs/funnel.js`. Run `node --test tests/*.test.cjs`.
- Emails and ad manifest: `docs/review/content/`. Primary copy: `docs/review/downloads/primary-copy.md`.
- Hub: edit `scripts/build_review.py` and `docs/review/review.css`; run `python3 scripts/build_review.py`.
- Pack: `python3 scripts/package_campaign.py`, optionally with `--output '/path/to/campaign folder'` to refresh a local handoff folder. The packaging script uses Pillow for reference contact sheets.

The page uses native dialog, FAQ controls and standard JavaScript. It needs no framework build or frontend application server. Real lead collection requires the client team's server integration before enabling live mode. The approval page and emails are not a launched funnel or activated sequence.

GTM `GTM-WJW6VTZ` and confirmed-opt-in tracking are prepared. See [PR-PREPARATION.md](PR-PREPARATION.md) for the proposed PR description and remaining client integration points. No PR has been opened.
