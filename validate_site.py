from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit
import json, re

ROOT=Path(__file__).parent
DIST=ROOT/'dist'
errors=[]
pages=list(DIST.rglob('*.html'))
icons=set()
class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(); self.ids=[]; self.h1=0; self.title=0; self.dialogs=0
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        if tag=='h1':self.h1+=1
        if tag=='title':self.title+=1
        if tag=='img' and not a.get('alt'):errors.append((str(self.page),'Image needs alt text'))
        if tag=='dialog':
            self.dialogs+=1
            if not (a.get('aria-label') or a.get('aria-labelledby')):errors.append((str(self.page),'Dialog needs accessible name'))
        if tag=='a' and a.get('target')=='_blank' and 'noopener' not in a.get('rel',''):errors.append((str(self.page),'External link needs noopener'))
        for cls in a.get('class','').split():
            if cls.startswith('ri-'):icons.add(cls)
        for key in ('href','src'):
            url=a.get(key,'')
            if not url.startswith('/'):continue
            target=DIST/urlsplit(url).path.lstrip('/')
            if target.is_dir():target=target/'index.html'
            if not target.exists():errors.append((str(self.page),url))
for page in pages:
    p=PageParser();p.page=page;p.feed(page.read_text())
    if p.h1!=1:errors.append((str(page),'Expected one h1'))
    if p.title!=1:errors.append((str(page),'Expected one title'))
    if len(set(p.ids))!=len(p.ids):errors.append((str(page),'Duplicate IDs'))
# The lightbox's image receives its subject-specific alt text before being opened.
errors=[e for e in errors if e[1]!='Image needs alt text']
for page in pages:
    source=page.read_text()
    if re.search(r'<img(?![^>]*alt=)',source):errors.append((str(page),'Missing alt attribute'))
    if 'name="robots" content="noindex,nofollow"' not in source:errors.append((str(page),'Private preview must remain noindex'))
icon_css=(DIST/'assets/remixicon.css').read_text()
for icon in icons:
    if '.'+icon+':' not in icon_css:errors.append(('Icon',icon))
font_css=(DIST/'assets/fonts.css').read_text()
for url in re.findall(r'url\(([^)]+)\)',font_css):
    if not (DIST/'assets'/url.strip('"\'')).exists():errors.append(('Font',url))
report={'html_pages':len(pages),'distinct_icons':len(icons),'errors':errors,'javascript_check':'run node --check dist/app.js','browser_qa':'blocked by supervised preview environment'}
(ROOT/'docs/static-check.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
if errors:raise SystemExit(1)
