"""Rebuild the approval hub from the public content and downloads in docs/review."""
from pathlib import Path
import json,re,html
ROOT=Path(__file__).resolve().parents[1]/'docs/review'
def esc(s):return html.escape(str(s),quote=True)
def inline(s):
    s=esc(s)
    s=re.sub(r'(https://[^\s<*]+)',r'<a href="\1" target="_blank" rel="noopener">\1</a>',s)
    s=re.sub(r'\*\*(.+?)\*\*',r'<strong>\1</strong>',s)
    s=re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)',r'<em>\1</em>',s)
    return s

def prose(s):
    blocks=[]
    for p in s.strip().split('\n\n'):
        if 'Book your Revival conversation → https://' in p:
            blocks.append('<p><a class="email-cta" href="https://go.riseupkings.com/scheduleyourcall" target="_blank" rel="noopener">Book your Revival conversation →</a></p>')
        elif all(re.match(r'^\d+\. ',l) for l in p.splitlines()):
            blocks.append('<ol>'+''.join('<li>'+inline(re.sub(r'^\d+\. ','',l))+'</li>' for l in p.splitlines())+'</ol>')
        elif all(l.startswith('- ') for l in p.splitlines()):
            blocks.append('<ul>'+''.join('<li>'+inline(l[2:])+'</li>' for l in p.splitlines())+'</ul>')
        else:blocks.append('<p>'+inline(p).replace('\n','<br>')+'</p>')
    return ''.join(blocks)

emails=json.loads((ROOT/'content/emails.json').read_text())
scripts=json.loads((ROOT/'content/scripts.json').read_text())
ads=json.loads((ROOT/'content/ads.json').read_text())

def grid(group):
    cards=[]
    for a in ads:
        if a['group']!=group:continue
        ref='A'+a['concept'][:2]
        path='ads/'+a['concept']+'.png'
        cards.append(f'''<article class="ad" id="{ref}"><a class="art" href="{path}" target="_blank" rel="noopener" aria-label="Open {ref}: {esc(a['headline'])} at full size"><img src="thumbnails/{a['concept']}.jpg" alt="{ref}: {esc(a['headline'])}" width="540" height="540" loading="lazy"></a><div class="ad-caption"><a class="ref" href="#{ref}">{ref}</a><span>1080 × 1080</span><a href="{path}" download>Download PNG ↓</a></div></article>''')
    return '<div class="ad-grid">'+''.join(cards)+'</div>'

def email_items():
    result=[]
    for i,e in enumerate(emails,1):
        ref=f'E{i:02}'
        result.append(f'''<details class="copy-item" id="{ref}" {'open' if i==1 else ''}><summary><span class="ref">{ref}</span><span class="summary-title">{esc(e['subject'])}<small>{esc(e['timing'])}</small></span><span class="toggle" aria-hidden="true">+</span></summary><div class="copy-inner"><dl class="email-meta"><dt>Subject</dt><dd>{esc(e['subject'])}</dd><dt>Preview text</dt><dd>{esc(e['preview'])}</dd></dl><div class="prose">{prose(e['body'])}</div><a class="permalink" href="#{ref}">Link to {ref} ↗</a></div></details>''')
    return ''.join(result)

def script_items():
    result=[]
    for i,s in enumerate(scripts,1):
        ref=f'S{i:02}'
        result.append(f'''<details class="copy-item" id="{ref}"><summary><span class="ref">{ref}</span><span class="summary-title">{esc(s['title'])}<small>Approx. {s['duration_seconds']} seconds · {s['spoken_words']} spoken words</small></span><span class="toggle" aria-hidden="true">+</span></summary><div class="copy-inner"><div class="prose">{prose(s['script'])}</div><a class="permalink" href="#{ref}">Link to {ref} ↗</a></div></details>''')
    return ''.join(result)

def primary_items():
    result=[]
    for block in (ROOT/'downloads/primary-copy.md').read_text().split('\n## ')[1:]:
        title,body=block.split('\n',1)
        ref=title[:3]
        result.append(f'''<details class="copy-item" id="{ref}"><summary><span class="ref">{ref}</span><span class="summary-title">{esc(title.split(' · ',1)[1])}<small>Primary text, headline and ad pairing</small></span><span class="toggle" aria-hidden="true">+</span></summary><div class="copy-inner"><div class="prose">{prose(body)}</div><a class="permalink" href="#{ref}">Link to {ref} ↗</a></div></details>''')
    return ''.join(result)

page='''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>Revival Campaign | Rise Up Kings Approval</title><meta name="description" content="Review the Revival landing page, 20 static ads, five emails, five video scripts and three primary-copy options."><link rel="icon" href="../images/ruk-logo.webp"><link rel="stylesheet" href="review.css"></head>
<body><a class="skip" href="#main">Skip to campaign materials</a>
<aside class="sidebar"><a class="brand" href="#overview"><img src="../images/ruk-logo.webp" alt="Rise Up Kings" width="152" height="72"><span>RUK MINISTRIES</span></a><div class="sidebar-title">REVIVAL<span>Campaign review</span></div><nav aria-label="Campaign materials"><a href="#landing">01 <span>Landing page</span><span>↗</span></a><a href="#ads">02 <span>Static ads</span><span>20</span></a><a href="#emails">03 <span>Emails</span><span>5</span></a><a href="#scripts">04 <span>Video scripts</span><span>5</span></a><a href="#primary">05 <span>Primary copy</span><span>3</span></a><a href="#sources">06 <span>Source notes</span><span>↗</span></a></nav><a class="sidebar-download" href="downloads/revival-campaign.zip" download>Download campaign ↓<small>ZIP · All campaign files</small></a><p class="sidebar-note">Prepared for Rise Up Kings<br>8 September 2026</p></aside>
<main id="main"><header id="overview"><div class="eyebrow">RISE UP KINGS / RUK MINISTRIES</div><div class="header-line"><h1>Revival campaign</h1><span class="status"><i></i> FOR APPROVAL</span></div><p class="intro">The page, the message, and the creative. Review every campaign asset below.</p><div class="review-note">For feedback, reference the item number — for example <a href="#A11">A11</a>, <a href="#E01">E01</a> or <a href="#S02">S02</a> — and the change you’d like.</div></header>
<section id="landing"><div class="section-heading"><div><span class="eyebrow">01 / THE DESTINATION</span><h2>Landing page</h2></div><a class="button" href="../" target="_blank" rel="noopener">Open landing page ↗</a></div><div class="landing-card"><div class="landing-text"><span class="eyebrow">REVIVAL · THREE DAYS FOR PASTORS</span><h3>The man behind<br>the ministry.</h3><p>The complete prospect-facing page, including the existing RUK Ministries application.</p><a href="../" target="_blank" rel="noopener">View the live page ↗</a></div><img src="../images/revival-room.jpg" alt="Prayer imagery published by RUK Ministries" width="800" height="530"></div><details class="page-preview"><summary>Preview the landing page here <span aria-hidden="true">+</span></summary><iframe title="Live Revival landing page preview" src="../" loading="lazy"></iframe></details><p class="small-note">The application is live. Please review without submitting sample details, as submission can start RUK’s follow-up.</p></section>
<section id="ads"><div class="section-heading"><div><span class="eyebrow">02 / CREATIVE</span><h2>Static ads <span class="count">20</span></h2></div><span class="section-detail">Click any ad to see it full size.</span></div><div class="group-heading"><h3>Short-copy variations</h3><span>A11–A20 · 10 ads</span></div><p class="section-intro">Fewer words. One clear message per creative.</p>'''+grid('short')+'''<div class="group-heading second-group"><h3>Original concepts</h3><span>A01–A10 · 10 ads</span></div><p class="section-intro">The earlier concepts, retained for comparison with pricing removed.</p>'''+grid('original')+'''<p class="small-note">The short-copy set uses typography. Some original concepts include AI-edited or illustrative scenes; these are creative imagery, not participant testimonials.</p></section>
<section id="emails"><div class="section-heading"><div><span class="eyebrow">03 / FOLLOW-UP</span><h2>Email sequence <span class="count">5</span></h2></div><a class="text-link" href="downloads/emails.md" download>Download emails ↓</a></div><p class="section-intro">For qualified applicants who have not booked a conversation. Draft sequence for approval; emails have not been activated.</p><div class="sequence"><span>Qualified application</span><b>→</b><span>Immediate</span><b>→</b><span>Day 1</span><b>→</b><span>Day 3</span><b>→</b><span>Day 5</span><b>→</b><span>Day 7</span></div>'''+email_items()+'''</section>
<section id="scripts"><div class="section-heading"><div><span class="eyebrow">04 / VIDEO</span><h2>Direct-response scripts <span class="count">5</span></h2></div><a class="text-link" href="downloads/scripts.md" download>Download scripts ↓</a></div><p class="section-intro">Five distinct angles. One complete script per angle, each around 60 seconds.</p>'''+script_items()+'''</section>
<section id="primary"><div class="section-heading"><div><span class="eyebrow">05 / AD TEXT</span><h2>Primary copy <span class="count">3</span></h2></div><a class="text-link" href="downloads/primary-copy.md" download>Download copy ↓</a></div><p class="section-intro">The text that runs alongside the creative, with headlines, descriptions and suggested ad pairings.</p>'''+primary_items()+'''</section>
<section id="sources"><div class="section-heading"><div><span class="eyebrow">06 / ACCURACY</span><h2>Source notes</h2></div><a class="text-link" href="downloads/source-checks.md" download>Download source checks ↓</a></div><div class="source-grid"><article><h3>Program details</h3><p>The three-day format, audience, Christ-centered approach and four pillars are grounded in the supplied Revival brief and <a href="https://rukministries.com/" target="_blank" rel="noopener">RUK Ministries website</a>.</p></article><article><h3>Pastor quotation</h3><p>Rob Satterfield’s short quotation is taken from his published Revival account on the Ministries website. No review totals, star ratings or guaranteed outcomes are used.</p></article><article><h3>Application &amp; booking</h3><p>The landing page uses the <a href="https://go.riseupkings.com/rukminapplication" target="_blank" rel="noopener">existing Ministries application</a>. Emails link to the <a href="https://go.riseupkings.com/scheduleyourcall" target="_blank" rel="noopener">existing scheduling page</a>.</p></article><article><h3>Campaign scope</h3><p>Pricing is omitted throughout this pack. Event dates are left for the team to confirm during the application process. No invented participant stories or results are included.</p></article></div></section>
<footer><span>RUK MINISTRIES · REVIVAL<br><small>Campaign materials for approval · 8 September 2026</small></span><a href="downloads/revival-campaign.zip" download>Download all campaign files ↓</a><a href="#overview">Back to top ↑</a></footer></main>
<script>function revealLinkedItem(){const id=decodeURIComponent(location.hash.slice(1));const item=document.getElementById(id);if(item&&item.tagName==='DETAILS'){item.open=true;}}window.addEventListener('hashchange',revealLinkedItem);revealLinkedItem();</script></body></html>'''
(ROOT/'index.html').write_text(page)
print('Built review/index.html: 20 ads, 5 emails, 5 scripts, 3 primary-copy options.')
