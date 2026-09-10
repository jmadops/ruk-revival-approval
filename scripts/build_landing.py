"""Combine the campaign opening with retained Ministries HTML/CSS sections.

Source snapshots and content exclusions: source/ministries/README.md.
No external fetch or HTML parser is needed to build.
"""
from pathlib import Path
import html
import json
root = Path(__file__).resolve().parents[1] / 'docs'
data = json.loads((root / 'content/ministries.json').read_text())
e = html.escape
star = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"></path></svg>'
cards = []
for review in data['google_reviews']:
    cards.append(f'''<article class="rukm-test-c__ticker-card" id="{e(review['id'])}">
      <div class="rukm-test-c__review-stars" role="img" aria-label="{review['rating']} out of 5 stars">{star * review['rating']}</div>
      <p class="rukm-test-c__review-text">“{e(review['quote'])}”</p>
      <div class="rukm-test-c__review-author"><span class="rukm-test-c__review-initial" aria-hidden="true">{e(review['name'][0])}</span><p class="rukm-test-c__review-name">{e(review['name'])}</p></div>
      <a class="revival-review-link" href="{e(review['url'])}" target="_blank" rel="noopener">Read full review on Google ↗</a>
    </article>''')
reviews = '''<div class="rukm-test-c__bottom" id="google-reviews"><div class="rukm-test-c__ticker-label"><span>Google reviews mentioning Revival</span></div><div class="rukm-test-c__container revival-review-grid">''' + ''.join(cards) + '''</div></div>'''
sections = (root / 'content/ministries-sections.html').read_text()
assert sections.count('<!-- GOOGLE_REVIEWS -->') == 1
sections = sections.replace('<!-- GOOGLE_REVIEWS -->', reviews)
page = (root / 'content/campaign-frame.html').read_text().replace('<!-- MINISTRIES_SECTIONS -->', sections)
(root / 'index.html').write_text(page)
print('Built campaign opening with original Ministries section layouts and linked Revival reviews.')
