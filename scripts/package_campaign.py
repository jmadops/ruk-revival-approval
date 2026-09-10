"""Refresh all client-facing files from repository sources; optionally sync an output folder."""
from pathlib import Path
import argparse,html,json,runpy,shutil,tempfile,zipfile
repo=Path(__file__).resolve().parents[1]
docs=repo/'docs';review=docs/'review'
parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path);args=parser.parse_args()
emails=json.loads((review/'content/emails.json').read_text())
scripts=json.loads((review/'content/scripts.json').read_text())
manifest=json.loads((review/'content/ads.json').read_text())
intro='# Revival opt-in emails for approval\n\nAudience: opted in; application not yet submitted.\n\nSend: immediate, day 1, day 3, day 5 and day 7. Stop on application submission.\n\nConfirmed application destination: https://go.riseupkings.com/rukminapplication. These drafts are not activated.\n\n'
def email_md(i,e):return f"## E{i:02} · {e['subject']}\n\n**Send:** {e['timing']}\n\n**Subject:** {e['subject']}\n\n**Preview:** {e['preview']}\n\n---\n\n{e['body']}\n"
combined=intro+'\n---\n\n'.join(email_md(i,e) for i,e in enumerate(emails,1))
(review/'downloads/emails.md').write_text(combined)
# The renderer is also the shared Markdown-to-readable-HTML formatter.
helpers=runpy.run_path(str(repo/'scripts/build_review.py'))
prose=helpers['prose']
def readable(title,note,items):
 css='body{font:16px/1.8 -apple-system,BlinkMacSystemFont,Arial,sans-serif;background:#f4f1e7;color:#222;margin:0;padding:40px 22px}main{max-width:780px;margin:auto}article{background:white;padding:30px;margin:25px 0;border-top:3px solid #b99a55}h1{line-height:1.15}h2{font-size:22px;line-height:1.4}p{margin:0 0 20px}small{color:#62665a}a{color:#826121}.email-cta{font-weight:bold}li{margin-bottom:12px}'
 return '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+html.escape(title)+'</title><style>'+css+'</style></head><body><main><h1>'+html.escape(title)+'</h1><p>'+html.escape(note)+'</p>'+''.join(items)+'</main></body></html>'
with tempfile.TemporaryDirectory(prefix='revival-pack-') as td:
 pack=Path(td)/'Revival Campaign';pack.mkdir()
 for name in ['Ads','Emails','Scripts','Landing Page','Review']:(pack/name).mkdir()
 for a in manifest:
  dest=pack/a['file'];dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(review/'ads'/f"{a['concept']}.png",dest)
 (pack/'Ads/ASSET-MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
 (pack/'Ads/READ-ME.md').write_text('# Revival ad selection\n\nSelected: A01–A10, original concepts with no pricing.\n\nArchived: A11–A20, earlier short-copy variations. Retained for reference, not for the current launch.\n\nThe original artwork is unchanged. Some concepts contain AI-edited or illustrative scenes.\n')
 # Reference sheets are generated from the exact approved PNGs without changing the ad artwork.
 from PIL import Image,ImageOps,ImageDraw
 for group,label,filename in [('original','SELECTED','SELECTED-CONTACT-SHEET.jpg'),('short','ARCHIVED','ARCHIVED-CONTACT-SHEET.jpg')]:
  selected=[a for a in manifest if a['group']==group]
  sheet=Image.new('RGB',(1500,680),(244,241,231));draw=ImageDraw.Draw(sheet)
  for i,a in enumerate(selected):
   with Image.open(review/'ads'/f"{a['concept']}.png") as im:thumb=ImageOps.contain(im.convert('RGB'),(280,280))
   x=(i%5)*300+10;y=(i//5)*335+10;sheet.paste(thumb,(x,y));draw.text((x,y+290),f"A{a['concept'][:2]}  {label}",fill=(40,40,30))
  sheet.save(pack/'Ads'/filename,quality=92)
 email_cards=[]
 for i,e in enumerate(emails,1):
  (pack/'Emails'/f"{e['id']}.md").write_text(email_md(i,e))
  body=prose(e['body'])
  email_cards.append('<article><small>'+html.escape(e['timing'])+'</small><h2>E%02d · '%i+html.escape(e['subject'])+'</h2><p><strong>Preview text:</strong> '+html.escape(e['preview'])+'</p>'+body+'</article>')
 (pack/'Emails/ALL-FIVE-EMAILS.md').write_text(combined)
 (pack/'Emails/READ-EMAILS.html').write_text(readable('Revival opt-in emails','For opt-ins who have not submitted an application. Application link confirmed. Not activated.',email_cards))
 script_md='# Revival scripts · Saved for later\n\nNot reviewed in detail by Will. Not part of current launch approval.\n\n'
 script_cards=[]
 for i,s in enumerate(scripts,1):
  block=f"## S{i:02} · {s['title']}\n\nSaved for later. Approx. {s['duration_seconds']} seconds; {s['spoken_words']} spoken words.\n\n{s['script']}\n"
  (pack/'Scripts'/f"{s['id']}.md").write_text(block);script_md+=block+'\n---\n\n'
  script_cards.append('<article><h2>S%02d · '%i+html.escape(s['title'])+'</h2>'+prose(s['script'])+'</article>')
 (pack/'Scripts/ALL-FIVE-SCRIPTS.md').write_text(script_md)
 (review/'downloads/scripts.md').write_text(script_md)
 (pack/'Scripts/READ-SCRIPTS.html').write_text(readable('Revival scripts · Saved for later','Five scripts for a future creative round. Not reviewed for launch.',script_cards))
 (pack/'Scripts/README.md').write_text('# Saved for later\n\nWill has not reviewed these scripts in detail. The copy is retained unchanged for a future creative round.\n')
 for f in ['index.html','landing.css','ministries.css','ministries-integration.css','ministries.js','tracking.js','funnel-config.js','funnel-core.js','funnel.js','application-preview.html']:
  shutil.copy2(docs/f,pack/'Landing Page'/f)
 for folder in ['images','fonts','content']:shutil.copytree(docs/folder,pack/'Landing Page'/folder)
 shutil.copy2(review/'downloads/primary-copy.md',pack/'PRIMARY-COPY.md')
 shutil.copy2(review/'downloads/source-checks.md',pack/'Review/SOURCE-CHECKS.md')
 shutil.copy2(review/'downloads/google-reviews.md',pack/'Review/GOOGLE-REVIEWS.md')
 shutil.copy2(repo/'HANDOFF.md',pack/'Review/TEAM-HANDOFF.md')
 shutil.copy2(repo/'PR-PREPARATION.md',pack/'Review/PR-PREPARATION.md')
 (pack/'Review/FUNNEL-CHECK.md').write_text('# Opt-in-first flow\n\nLanding page → name/email/phone modal → application. The approval version is a preview only: no contact details are sent or saved. The application destination is https://go.riseupkings.com/rukminapplication. The preview opens that application without saving the sample details. The production capture endpoint and consent setup remain with RUK’s team.\n\nEmails run only while the application has not been submitted. See TEAM-HANDOFF.md for the integration contract and the four repositories checked.\n')
 (pack/'Review/QA.md').write_text('# Validation\n\nThe form checks name, email and phone. Automated tests cover preview isolation, accepted lead capture, invalid input, missing configuration, failed responses and timeouts. No real leads were submitted.\n\nOriginal ad image checksums are preserved. Active campaign copy has no pricing or event dates. The application destination is confirmed; production lead capture and email automation are not connected.\n')
 (pack/'README.md').write_text('# Revival campaign · Revised 10 September 2026\n\nApproval hub: https://jmadops.github.io/ruk-revival-approval/review/\n\nLanding page: https://jmadops.github.io/ruk-revival-approval/\n\n- Ads A01–A10: selected original concepts, no pricing.\n- Ads A11–A20: archived for reference.\n- Five revised opt-in emails: continue the application; not activated.\n- Three primary-copy options: accepted copy, paired with selected ads.\n- Five scripts: saved for later, not reviewed for launch.\n- Landing page: original Ministries section designs with the campaign opening. Opt-in preview opens the confirmed application; lead capture pending.\n\nSee Review/TEAM-HANDOFF.md for the client PR setup.\n')
 with zipfile.ZipFile(review/'downloads/revival-campaign.zip','w',zipfile.ZIP_DEFLATED) as z:
  for f in sorted(pack.rglob('*')):
   if f.is_file():z.write(f,str(f.relative_to(pack.parent)))
 if args.output:
  # Preserve files outside the revised deliverable paths (including prior-version archives).
  for f in pack.rglob('*'):
   if f.is_file():
    dest=args.output/f.relative_to(pack);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(f,dest)
  print('Refreshed campaign folder:',args.output)
print('Updated copy previews, selected/archived ad pack and ZIP download.')
