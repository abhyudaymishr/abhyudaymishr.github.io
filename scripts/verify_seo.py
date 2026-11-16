"""Audit rendered on-page SEO; does not predict rankings or Google index status."""
import argparse
from collections import Counter, defaultdict
from html.parser import HTMLParser
import json
from pathlib import Path
from urllib.parse import urljoin, urlparse

class SEOPage(HTMLParser):
    def __init__(self, url):
        super().__init__(convert_charrefs=True)
        self.url=url; self.title=''; self.h1=''; self.description=''; self.robots=''
        self.meta={}; self.links=[]; self.schemas=[]; self.h2s=0
        self._title=False; self._h1=False; self._main=False; self._schema=None
    def handle_starttag(self, tag, pairs):
        a=dict(pairs)
        if tag=='title': self._title=True
        if tag=='h1': self._h1=True
        if tag=='h2': self.h2s+=1
        if tag=='main': self._main=True
        if tag=='meta': self.meta[a.get('name') or a.get('property')]=a.get('content','')
        if tag=='a' and self._main and a.get('href'): self.links.append(urljoin(self.url,a['href']))
        if tag=='script' and a.get('type')=='application/ld+json': self._schema=''
    def handle_endtag(self, tag):
        if tag=='title': self._title=False
        if tag=='h1': self._h1=False
        if tag=='main': self._main=False
        if tag=='script' and self._schema is not None:
            self.schemas.append(json.loads(self._schema)); self._schema=None
    def handle_data(self, text):
        if self._title: self.title+=text
        if self._h1: self.h1+=text
        if self._schema is not None: self._schema+=text
    def finish(self):
        self.title=' '.join(self.title.split()); self.h1=' '.join(self.h1.split())
        self.description=self.meta.get('description',''); self.robots=self.meta.get('robots','')


def audit(root):
    index=json.loads((root/'content-index.json').read_text())
    origin=index['url'].rstrip('/')
    pages={}
    for file in root.rglob('*.html'):
        rel='/'+file.relative_to(root).as_posix()
        if rel.endswith('index.html'): rel=rel[:-10]
        page=SEOPage(origin+rel); page.feed(file.read_text()); page.finish()
        if 'noindex' not in page.robots: pages[page.url]=page
    titles=Counter(p.title.casefold() for p in pages.values())
    descriptions=Counter(p.description.casefold() for p in pages.values())
    inbound=defaultdict(set)
    for page in pages.values():
        for ref in page.links:
            parsed=urlparse(ref); target=parsed._replace(query='',fragment='').geturl()
            if target in pages and target!=page.url: inbound[target].add(page.url)
    errors=[]; warnings=[]; rows=[]
    for url,page in sorted(pages.items()):
        if not page.title or titles[page.title.casefold()]!=1: errors.append(f'{url}: missing or duplicate title')
        if not page.description or descriptions[page.description.casefold()]!=1: errors.append(f'{url}: missing or duplicate description')
        if len(page.title)>70: warnings.append(f'{url}: title exceeds the editorial 70-character budget')
        if not 70<=len(page.description)<=180: warnings.append(f'{url}: description is outside the editorial 70–180-character range')
        if url!=origin+'/' and not inbound[url]: errors.append(f'{url}: no incoming link from another indexable page’s main content')
        graph=[entity for schema in page.schemas for entity in schema.get('@graph',[])]
        work=next((e for e in graph if e.get('@type') in ('BlogPosting','ScholarlyArticle','CreativeWork')),None)
        if work and work.get('headline')!=page.h1: errors.append(f'{url}: work headline differs from the visible H1')
        if work and not work.get('author'): errors.append(f'{url}: work author missing')
        rows.append({'url':url,'title':page.title,'title_characters':len(page.title),'description':page.description,'description_characters':len(page.description),'h1':page.h1,'section_headings':page.h2s,'incoming_content_pages':len(inbound[url]),'schema_types':[e.get('@type') for e in graph]})
    # Publication removals must also stay out of discovery resources.
    if any('Geometry-Induced Sparse Attention for PDE Operators'==item['title'] for item in index['items']): errors.append('The withdrawn draft is present in the content index')
    return {'scope':'Rendered HTML on-page checks; character budgets are editorial heuristics, not search engine ranking requirements.','indexable_pages':len(pages),'duplicate_titles':sum(v-1 for v in titles.values() if v>1),'duplicate_descriptions':sum(v-1 for v in descriptions.values() if v>1),'errors':errors,'warnings':warnings,'pages':rows}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory',nargs='?',default='_site')
    parser.add_argument('--report',type=Path)
    args=parser.parse_args(); report=audit(Path(args.directory))
    if args.report:
        args.report.parent.mkdir(parents=True,exist_ok=True)
        args.report.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    for message in report['errors']: print('ERROR:',message)
    for message in report['warnings']: print('REVIEW:',message)
    print(f"On-page SEO: {report['indexable_pages']} pages; {len(report['errors'])} errors; {len(report['warnings'])} editorial review items. No ranking or indexing score is inferred.")
    raise SystemExit(bool(report['errors']))

if __name__=='__main__': main()
