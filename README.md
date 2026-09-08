# Revival approval landing page

Live review: https://jmadops.github.io/ruk-revival-approval/

A price-free RUK Ministries Revival landing page for approval. GitHub Pages serves the static files in `docs/` from `main`.

- The landing page is public and shareable, with a noindex directive.
- Every application CTA goes to the on-page application section.
- The iframe uses the existing RUK Ministries application at https://go.riseupkings.com/rukminapplication and provides a separate-window fallback.
- Applications are handled by RUK’s existing Ontraport form. GitHub does not store applicant data.
- The quote is a verified excerpt from Sr Pastor Rob Satterfield’s Revival account on https://rukministries.com/.
- No price, referral offer, star rating, review count, availability claim, or invented participant result is included.

## Updating the page

Edit the static `docs/index.html`, `docs/styles.css`, or assets and push to `main`. GitHub Pages republishes that folder. The page uses native anchor links and FAQ controls, so it needs no frontend build or application server.

The form is live. Reviewers should not submit sample contact details: doing so can start RUK’s existing follow-up process.
