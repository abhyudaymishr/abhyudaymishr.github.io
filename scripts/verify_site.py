"""Check the actual Jekyll output before deployment; Python standard library only."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse, unquote, urljoin
import json
import os
import struct
import sys
import xml.etree.ElementTree as ET

root = Path(sys.argv[1] if len(sys.argv) > 1 else '_site').resolve()
origin = 'https://abhyudaymishr.github.io'
errors = []

def require(condition, message):
    if not condition:
        errors.append(message)

class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids=set(); self.refs=[]; self.meta={}; self.canonical=[]; self.title=''; self.h1=0; self.main=0; self.in_title=False; self.in_schema=False; self.schemas=[]; self.schema=''
    def handle_starttag(self, tag, pairs):
        a=dict(pairs)
        if a.get('id'):
            require(a['id'] not in self.ids, f'Duplicate id {a["id"]} in {self.file}')
            self.ids.add(a['id'])
        if tag=='h1': self.h1+=1
        if tag=='main': self.main+=1
        if tag=='title': self.in_title=True
        if tag=='meta': self.meta[a.get('name') or a.get('property')]=a.get('content','')
        if tag=='link' and a.get('rel')=='canonical': self.canonical.append(a.get('href'))
        if tag=='script' and a.get('type')=='application/ld+json': self.in_schema=True;self.schema=''
        if tag=='img':
            require('alt' in a, f'Missing image alt in {self.file}')
            require(a.get('width') and a.get('height'), f'Image dimensions absent in {self.file}')
        if tag in ('a','link','script','img','form'):
            ref=a.get('src') or a.get('href') or a.get('action')
            if ref: self.refs.append(ref)
    def handle_endtag(self, tag):
        if tag=='title': self.in_title=False
        if tag=='script' and self.in_schema: self.schemas.append(json.loads(self.schema));self.in_schema=False
    def handle_data(self, text):
        if self.in_title: self.title+=text
        if self.in_schema: self.schema+=text

pages={}
for file in root.rglob('*.html'):
    rel='/' + file.relative_to(root).as_posix()
    url=rel[:-10] if rel.endswith('index.html') else rel
    parser=Page();parser.file=rel
    try: parser.feed(file.read_text())
    except (ValueError, json.JSONDecodeError) as error: errors.append(f'{rel}: {error}');continue
    pages[url]=parser
    require(parser.h1==1, f'{rel}: expected one H1; got {parser.h1}')
    require(parser.main==1, f'{rel}: expected one main landmark')
    require(len(parser.canonical)==1 and parser.canonical[0]==origin+url, f'{rel}: incorrect canonical URL')
    require(bool(parser.title.strip()) and bool(parser.meta.get('description')), f'{rel}: missing title or description')
    require(parser.schemas, f'{rel}: missing structured data')
    if parser.schemas:
        graph=parser.schemas[0]['@graph']
        require(any(x['@type']=='Person' for x in graph),f'{rel}: missing author entity')
    require('main-content' in parser.ids, f'{rel}: skip-link target absent')
    if url!='/404.html': require('noindex' in parser.meta.get('robots','') or 'index,follow' in parser.meta.get('robots',''),f'{rel}: missing robots directive')

def resolve(ref, source='/'):
    url=urlparse(urljoin(origin+source,ref))
    if url.scheme not in ('http','https') or url.netloc!=urlparse(origin).netloc: return None,None,None
    path=unquote(url.path)
    target=root/path.lstrip('/')
    if path.endswith('/'): target=target/'index.html'
    return path,url.fragment,target

for url, page in pages.items():
    for ref in page.refs:
        path,fragment,target=resolve(ref,url)
        if target is None: continue
        require(target.exists(), f'{url}: missing local target {ref}')
        if fragment and path in pages: require(unquote(fragment) in pages[path].ids, f'{url}: missing anchor {ref}')

sitemap=ET.parse(root/'sitemap.xml').getroot()
locations=[e.text for e in sitemap.findall('{*}url/{*}loc')]
require(len(locations)==len(set(locations)), 'Duplicate sitemap URLs')
expected={origin+url for url,p in pages.items() if 'noindex' not in p.meta.get('robots','')}
require(set(locations)==expected, 'Sitemap must contain all and only indexable pages')
feed=ET.parse(root/'feed.xml').getroot()
require(len(feed.findall('{*}entry'))>0,'Feed has no entries')
index=json.loads((root/'content-index.json').read_text())
require(len(index['items'])==len(expected),'Content index coverage differs from public pages')
for item in index['items']:
    require(item['url'] in expected, f'Index has unknown/nonindexable page: {item["url"]}')
    require(bool(item['description']),f'Empty index description: {item["url"]}')
    require('{{' not in item['text'] and '{%' not in item['text'], f'Raw template in content index: {item["url"]}')
for name in ('llms.txt','llms-full.txt','robots.txt'):
    text=(root/name).read_text();require('{{' not in text and '{%' not in text,f'Unrendered Liquid in {name}')
require('/sitemap.xml' in (root/'robots.txt').read_text(),'robots.txt lacks sitemap')
require(not (root/'scripts').exists() and not (root/'tests').exists() and not (root/'README.html').exists(),'Development files exposed in build')
png=(root/'assets/images/seo-card.png').read_bytes()
require(png[:8]==b'\x89PNG\r\n\x1a\n' and struct.unpack('>II',png[16:24])==(1200,630),'Social card must be a 1200 × 630 PNG')
require((root/'assets/images/structure.svg').stat().st_size < 250_000, 'Hero asset exceeded size budget')
summary_path = os.environ.get('GITHUB_STEP_SUMMARY')

if errors:
    print('\n'.join(errors))
    if summary_path:
        with open(summary_path, 'a', encoding='utf-8') as f:
            f.write("### ❌ Site Verification Failed\n\n")
            for err in errors:
                f.write(f"- {err}\n")
    sys.exit(1)

success_msg = f'Verified {len(pages)} HTML pages, {len(locations)} sitemap URLs, {len(index["items"])} index entries, all internal links/anchors, JSON-LD, feed, and social card.'
print(success_msg)

if summary_path:
    with open(summary_path, 'a', encoding='utf-8') as f:
        f.write("### ✅ Site Verification Passed\n\n")
        f.write(f"- **HTML Pages**: {len(pages)} pages verified (H1, main landmark, title, meta description, skip link)\n")
        f.write(f"- **Sitemap**: {len(locations)} URLs matching indexable pages exactly\n")
        f.write(f"- **Search Index**: {len(index['items'])} entries validated\n")
        f.write(f"- **AI Discovery**: `llms.txt`, `llms-full.txt`, and `robots.txt` validated\n")
        f.write(f"- **Structured Data**: JSON-LD Person schema verified\n")
        f.write(f"- **Internal Links & Anchors**: All local references resolved\n")
        f.write(f"- **Visual Assets**: 1200×630 PNG card and SVG hero verified within budget\n")
