# Retained Ministries sections

Source: https://rukministries.com/ — retrieved 10 September 2026.

These are the actual section HTML and associated scoped styles from the live homepage. SVG viewBox case is normalized. The deployable CSS retains the source rules, with image URLs changed to the identical local assets. Oswald weights 400/500/600/700 come from the source page’s Google Fonts family; Inter is already local.

The campaign frame keeps the accepted hero, video, opening copy, final CTA and opt-in. `docs/content/ministries-sections.html` retains the original lower-section structures. The integration stylesheet only isolates inherited typography, supports semantic CTA buttons, lays out the three sourced Google cards, and prevents FAQ answers being clipped.

## Limited differences from the original sections

- Apply anchors become buttons opening the existing KSP-style opt-in. The confirmed application URL is in funnel-config.js.
- The full training-room photograph stays a background behind the Our Approach glass card. The Ministries section’s original background is also retained.
- Generic Google rating totals and general-event ticker reviews are replaced with the three previously verified Revival excerpts, using the original dark-card styles. Cards are stationary so reviewers can read them and open the sources.
- Pastor cards keep their source layout. Decorative stars are removed because these website accounts are not evidenced Google ratings. Rob’s excerpt retains the approved ending before the reference to money.
- Previous exclusions remain: generic scale/non-profit claims and guaranteed-result wording are not reintroduced. The Ministries subtitle and description use the previously approved scope; FAQ answers retain the prior price-free, date-free wording.
- FAQ markup adds accessible expanded state and uses a small script instead of inline click handlers.
- The original Two Ways/financial-support section, event dates, pricing, countdowns and press-logo claims remain excluded as previously directed.

No client repository or live Ministries homepage was modified. This is Jay’s approval copy, ready for RUK’s team to integrate through their normal PR process.
