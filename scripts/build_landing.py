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

# Build the separate campaign variant for leaders of Christian men's
# organizations while preserving the original pastor-focused page.
leader_sections = (root / 'content/ministries-sections.html').read_text()
start = leader_sections.index('<!-- PASTOR_TESTIMONIALS_START -->')
end_marker = '<!-- PASTOR_TESTIMONIALS_END -->'
end = leader_sections.index(end_marker) + len(end_marker)
leader_sections = leader_sections[:start] + leader_sections[end:]
leader_replacements = {
    'Pastoral leadership, while rewarding, comes with its unique set of challenges. At RUK Ministries, we understand these struggles and are committed to helping you navigate them. Our 3-day intensive event is designed to address these pain points head-on, providing you with the tools and strategies to overcome them and thrive in your calling.':
        "Leading men toward Christ is meaningful work, but carrying other men's burdens can make it easy to neglect your own. Revival is a three-day intensive designed to help Christian men's ministry leaders confront what has been pushed aside, strengthen the man behind the mission, and return ready to lead from a healthier place.",
    'Pastors Apply Here': 'Ministry Leaders Apply Here',
    '<span class="rukm-empower-b__gold">Empowering Pastors</span> to Overcome Unique Challenges and <span class="rukm-empower-b__gold">Thrive in Their Calling</span>':
        '<span class="rukm-empower-b__gold">Strengthening Men\'s Ministry Leaders</span> to Serve with Conviction and <span class="rukm-empower-b__gold">Thrive in Their Calling</span>',
    'The weight of spiritual leadership can often lead to feelings of isolation and an unwillingness to admit struggles. We provide a supportive community where you can share your journey with like-minded individuals, fostering openness and humility.':
        'When other men look to you for strength, admitting your own struggles can feel complicated. Revival gives you a trusted brotherhood where honesty is met with support, challenge, and humility.',
    'Striking a balance between family responsibilities and pastoral duties can be challenging. We offer practical strategies to ensure both aspects are healthy.':
        'The mission can follow you home. Revival helps you lead with purpose while staying present and connected with your wife and children.',
    "Ministers' finances are more complicated than the average person and financial management can be a daunting task. Our event includes deep dives into finance topics, equipping you with the knowledge to be a great steward.":
        'Financial pressure can quietly drain your focus and confidence. Revival gives you practical tools to build stronger habits and steward what God has entrusted to you.',
    'Amidst the demands of pastoral duties, physical health often takes a back seat. We emphasize the importance of fitness and provide guidance on maintaining physical health.':
        'Serving others can push your physical health to the bottom of the list. Revival helps you rebuild the discipline and energy required to lead well for the long haul.',
    'Even as spiritual leaders, maintaining a consistent and intimate relationship with God can be challenging. We provide tools to strengthen your spiritual formation and deepen your relationship with God.':
        'Leading spiritual work does not automatically keep your own relationship with God strong. Revival creates space to renew your faith and reconnect with the reason you answered the call.',
    'For pastors and ministry leaders.': 'For leaders of Christian men\'s organizations.',
    'Do you find it difficult to stay balanced serving your congregation while staying connected to your wife and kids?':
        'Do you find it difficult to serve the mission while staying connected to your wife and kids?',
    'RUK Ministries is a non-denominational Christian organization. We welcome pastors and spiritual leaders from all biblical-based faiths. Our teachings and programs are based on biblical principles with Jesus Christ at the core.':
        'RUK Ministries is a non-denominational Christian organization. We welcome men who lead or serve Christian men through nonprofits, outreach ministries, discipleship groups, ministry networks, retreats, and other Bible-based organizations. Our teaching is grounded in biblical principles with Jesus Christ at the core.',
    'The event focuses on pastoral duties, personal life, and spiritual growth, with strategies around leadership, finance, and personal development. It aims to reignite your passion for your calling and equip you with tools to live a balanced and fulfilling life.':
        'The event focuses on the man behind the mission: his faith, family, fitness, finances, and leadership. It is designed to reignite your passion for your calling and equip you to lead from a stronger, healthier foundation.',
    'Revival is a three-day, in-person intensive for male pastors and ministry leaders.':
        "Revival is a three-day, in-person intensive for men who lead or serve through Christian men's organizations and ministries."
}
for old, new in leader_replacements.items():
    assert old in leader_sections, f'Missing leader section source text: {old}'
    leader_sections = leader_sections.replace(old, new)
leader_sections = leader_sections.replace('<!-- GOOGLE_REVIEWS -->', reviews)

leader_frame = (root / 'content/campaign-frame.html').read_text()
frame_replacements = {
    '<title>Revival | The Man Behind the Ministry | RUK Ministries</title>':
        "<title>Revival | For Christian Men's Ministry Leaders | RUK Ministries</title>",
    'content="A three-day, Christ-centered intensive for male pastors and ministry leaders. Faith, Family, Fitness, and Finances."':
        "content=\"A three-day, Christ-centered intensive for leaders of Christian men's organizations. Faith, Family, Fitness, and Finances.\"",
    '<a href="#stories">Pastor stories</a>': '<a href="#stories">Revival stories</a>',
    'THREE DAYS FOR MALE PASTORS &amp; MINISTRY LEADERS': 'THE RISE UP KINGS REVIVAL',
    'The church gets<br>your best.<br><em>What’s left for you?</em>': 'Christian Men’s<br>Ministry Leaders:<br><em>Strengthen the Man<br>Behind the Mission.</em>',
    'Everyone knows where to find you when something goes wrong. Your own struggles can stay out of the conversation. Revival gives the man behind the pulpit three days to confront what ministry has pushed aside.':
        "A three-day, Christ-centered intensive for men who lead other men through nonprofits, outreach ministries, discipleship groups, retreats, and Christian organizations.",
    '<strong>FOR PASTORS</strong><span>The man behind the ministry.</span>':
        '<strong>FOR MEN’S LEADERS</strong><span>The man behind the mission.</span>',
    'THE PASTOR BEHIND THE PULPIT': 'THE MAN BEHIND THE MISSION',
    'You can’t lead<br>a church while<br><em>running on empty.</em>': 'You can’t lead<br>other men while<br><em>running on empty.</em>',
    'The sermon still needs preparing. The phone keeps ringing. Someone always needs your attention.':
        'The next gathering needs planning. The messages keep coming. Someone always needs your attention.',
    'But at home, your mind is still in the meeting. Your Bible is open, and you’re already thinking about what somebody else needs to hear. There are things you need to say out loud, but your title makes honesty feel complicated.':
        'At home, your mind is still on the men you serve. Your Bible is open, and you are already thinking about what somebody else needs to hear. There are things you need to say out loud, but being the leader makes honesty feel complicated.',
    'The public ministry can keep performing long after the private man starts paying for it.':
        'The mission can keep moving long after the private man starts paying for it.',
    'FOR THE MAN BEHIND THE MINISTRY': 'FOR THE MAN BEHIND THE MISSION',
    'Three days. Four pillars. An honest look at the life behind the calling.':
        'Three days. Four pillars. An honest look at the life behind your leadership.',
    'then continue to tell us about your ministry.':
        'then continue to tell us about your leadership.'
}
for old, new in frame_replacements.items():
    assert old in leader_frame, f'Missing leader frame source text: {old}'
    leader_frame = leader_frame.replace(old, new)
leader_page = leader_frame.replace('<!-- MINISTRIES_SECTIONS -->', leader_sections)
(root / 'leaders.html').write_text(leader_page)

print('Built pastor and Christian men\'s ministry leader landing-page variants.')
