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

# Keep every element except the hero message identical so VWO can isolate the
# effect of the two results-led headlines Will approved on 23 September.
headline_variants = [
    {
        'file': 'pastor-reignite.html',
        'title': 'Revival | Reignite Your Passion for Ministry | RUK Ministries',
        'headline': 'In Three Days,<br><em>Reignite Your Passion<br>for Ministry and Restore<br>Your Work‑Life Harmony</em>',
        'copy': 'A life-transforming three-day experience designed specifically for pastors who are ready to feel fully alive in their calling again.',
    },
    {
        'file': 'pastor-burnout.html',
        'title': 'Revival | For Burned-Out Pastors | RUK Ministries',
        'headline': 'How Burned-Out Pastors<br><em>Are Reigniting Their Passion for Ministry<br>in Just Three Days</em>',
        'copy': 'So they can serve their church without sacrificing their family.',
    },
]
control_title = '<title>Revival | The Man Behind the Ministry | RUK Ministries</title>'
control_headline = '<h1>The church gets<br>your best.<br><em>What’s left for you?</em></h1>'
control_copy = '<p class="hero-copy">Everyone knows where to find you when something goes wrong. Your own struggles can stay out of the conversation. Revival gives the man behind the pulpit three days to confront what ministry has pushed aside.</p>'
for variant in headline_variants:
    assert control_title in page and control_headline in page and control_copy in page
    variant_page = page.replace(control_title, f'<title>{variant["title"]}</title>')
    variant_page = variant_page.replace(control_headline, f'<h1>{variant["headline"]}</h1>')
    variant_page = variant_page.replace(control_copy, f'<p class="hero-copy">{variant["copy"]}</p>')
    (root / variant['file']).write_text(variant_page)

# Build the separate campaign variant for Christian men serving through
# mission-driven organizations while preserving the pastor-focused page.
leader_sections = (root / 'content/ministries-sections.html').read_text()
start = leader_sections.index('<!-- PASTOR_TESTIMONIALS_START -->')
end_marker = '<!-- PASTOR_TESTIMONIALS_END -->'
end = leader_sections.index(end_marker) + len(end_marker)
leader_sections = leader_sections[:start] + leader_sections[end:]
leader_replacements = {
    'Pastoral leadership, while rewarding, comes with its unique set of challenges. At RUK Ministries, we understand these struggles and are committed to helping you navigate them. Our 3-day intensive event is designed to address these pain points head-on, providing you with the tools and strategies to overcome them and thrive in your calling.':
        "Serving people in Christ's name is meaningful work, but carrying the needs of others can make it easy to neglect your own. Revival is a three-day intensive designed to help Christian men confront what has been pushed aside, strengthen the man behind the mission, and return ready to serve from a healthier place.",
    'Pastors Apply Here': 'Christian Men Apply Here',
    'Unmasking the <span class="rukm-approach-b3__gold">Struggles</span> of <span class="rukm-approach-b3__gold">Spiritual</span> Leadership':
        'The <span class="rukm-approach-b3__gold">Hidden Cost</span> of <span class="rukm-approach-b3__gold">Serving</span> Others',
    '<span class="rukm-empower-b__gold">Empowering Pastors</span> to Overcome Unique Challenges and <span class="rukm-empower-b__gold">Thrive in Their Calling</span>':
        '<span class="rukm-empower-b__gold">Strengthening Christian Men</span> Who Serve Others and <span class="rukm-empower-b__gold">Live Their Calling</span>',
    'The weight of spiritual leadership can often lead to feelings of isolation and an unwillingness to admit struggles. We provide a supportive community where you can share your journey with like-minded individuals, fostering openness and humility.':
        'When people count on you to be strong, admitting your own struggles can feel complicated. Revival gives you a trusted brotherhood where honesty is met with support, challenge, and humility.',
    'Striking a balance between family responsibilities and pastoral duties can be challenging. We offer practical strategies to ensure both aspects are healthy.':
        'The work can follow you home. Revival helps you serve with purpose while staying present and connected with your wife and children.',
    "Ministers' finances are more complicated than the average person and financial management can be a daunting task. Our event includes deep dives into finance topics, equipping you with the knowledge to be a great steward.":
        'Financial pressure can quietly drain your focus and confidence. Revival gives you practical tools to build stronger habits and steward what God has entrusted to you.',
    'Amidst the demands of pastoral duties, physical health often takes a back seat. We emphasize the importance of fitness and provide guidance on maintaining physical health.':
        'Serving others can push your physical health to the bottom of the list. Revival helps you rebuild the discipline and energy required to keep showing up well for the long haul.',
    'Even as spiritual leaders, maintaining a consistent and intimate relationship with God can be challenging. We provide tools to strengthen your spiritual formation and deepen your relationship with God.':
        'Doing faith-driven work does not automatically keep your own relationship with God strong. Revival creates space to renew your faith and reconnect with the reason you answered the call.',
    'For pastors and ministry leaders.': 'For Christian men serving through mission-driven organizations.',
    'Do you find it difficult to stay balanced serving your congregation while staying connected to your wife and kids?':
        'Do you find it difficult to serve others while staying connected to your wife and kids?',
    'RUK Ministries is a non-denominational Christian organization. We welcome pastors and spiritual leaders from all biblical-based faiths. Our teachings and programs are based on biblical principles with Jesus Christ at the core.':
        'RUK Ministries is a non-denominational Christian organization. We welcome Christian men who serve through charities, nonprofits, missions, outreach organizations, foster-care work, recovery programs, community programs, and other faith-driven organizations. You do not need to be a pastor or hold a leadership title. Our teaching is grounded in biblical principles with Jesus Christ at the core.',
    'The event focuses on pastoral duties, personal life, and spiritual growth, with strategies around leadership, finance, and personal development. It aims to reignite your passion for your calling and equip you with tools to live a balanced and fulfilling life.':
        'The event focuses on the man behind the mission: his faith, family, fitness, finances, and personal life. It is designed to renew your strength and help you serve from a healthier foundation.',
    'Revival is a three-day, in-person intensive for male pastors and ministry leaders.':
        'Revival is a three-day, in-person intensive for Christian men who serve through charities, nonprofits, missions, outreach organizations, and other faith-driven work.',
    '<h3 class="rukm-empower-b__row-title">Balancing Family and Ministry</h3>':
        '<h3 class="rukm-empower-b__row-title">Balancing Family and Service</h3>',
    'After the event, you will have the opportunity to join the RUK Ministries community, a brotherhood of Christian leaders committed to supporting each other in their journey of faith and leadership. We offer ongoing training, seminars, and webinars to support your continued growth.':
        'After the event, you will have the opportunity to join the RUK Ministries community, a brotherhood of Christian men committed to supporting each other in faith, family, health, and purpose. We offer ongoing training, seminars, and webinars to support your continued growth.',
    'Have you considered leaving ministry altogether?':
        'Have you considered walking away from the work altogether?'
}
for old, new in leader_replacements.items():
    assert old in leader_sections, f'Missing leader section source text: {old}'
    leader_sections = leader_sections.replace(old, new)
leader_sections = leader_sections.replace('<!-- GOOGLE_REVIEWS -->', reviews)

leader_frame = (root / 'content/campaign-frame.html').read_text()
frame_replacements = {
    '<title>Revival | The Man Behind the Ministry | RUK Ministries</title>':
        '<title>Revival | For Christian Men Who Serve Others | RUK Ministries</title>',
    'content="A three-day, Christ-centered intensive for male pastors and ministry leaders. Faith, Family, Fitness, and Finances."':
        'content="A three-day, Christ-centered intensive for Christian men serving through charities, nonprofits, missions, outreach organizations, and other faith-driven work."',
    '<a href="#stories">Pastor stories</a>': '<a href="#stories">Revival stories</a>',
    'THREE DAYS FOR MALE PASTORS &amp; MINISTRY LEADERS': 'THE RISE UP KINGS REVIVAL',
    'The church gets<br>your best.<br><em>What’s left for you?</em>': 'Christian Men<br>Who Serve Others:<br><em>Strengthen the Man<br>Behind the Mission.</em>',
    'Everyone knows where to find you when something goes wrong. Your own struggles can stay out of the conversation. Revival gives the man behind the pulpit three days to confront what ministry has pushed aside.':
        'A three-day, Christ-centered intensive for men serving through charities, nonprofits, missions, outreach organizations, foster-care work, recovery programs, and other Christian organizations.',
    '<strong>FOR PASTORS</strong><span>The man behind the ministry.</span>':
        '<strong>FOR MEN WHO SERVE</strong><span>The man behind the mission.</span>',
    'THE PASTOR BEHIND THE PULPIT': 'THE MAN BEHIND THE MISSION',
    'You can’t lead<br>a church while<br><em>running on empty.</em>': 'You can’t serve<br>others while<br><em>running on empty.</em>',
    'The sermon still needs preparing. The phone keeps ringing. Someone always needs your attention.':
        'The next need is already waiting. The messages keep coming. Someone always needs your attention.',
    'But at home, your mind is still in the meeting. Your Bible is open, and you’re already thinking about what somebody else needs to hear. There are things you need to say out loud, but your title makes honesty feel complicated.':
        'At home, your mind is still on the people you serve. Your Bible is open, and you are already thinking about what somebody else needs. There are things you need to say out loud, but being the strong one makes honesty feel complicated.',
    'The public ministry can keep performing long after the private man starts paying for it.':
        'The mission can keep moving long after the private man starts paying for it.',
    'FOR THE MAN BEHIND THE MINISTRY': 'FOR THE MAN BEHIND THE MISSION',
    'Three days. Four pillars. An honest look at the life behind the calling.':
        'Three days. Four pillars. An honest look at the life behind your service.',
    'then continue to tell us about your ministry.':
        'then continue to tell us about your work.'
}
for old, new in frame_replacements.items():
    assert old in leader_frame, f'Missing leader frame source text: {old}'
    leader_frame = leader_frame.replace(old, new)
leader_page = leader_frame.replace('<!-- MINISTRIES_SECTIONS -->', leader_sections)
(root / 'leaders.html').write_text(leader_page)

print('Built pastor and Christian organization landing-page variants.')
