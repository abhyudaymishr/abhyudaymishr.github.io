# Search visibility audit — 16 November 2026

The live GitHub Pages site was reachable and crawlable at the time of the audit. The remaining source improvements address content clarity, search presentation, internal discovery, and preservation of metadata during publishing. Local check results are not a Google ranking or indexing score.

## Live-site findings

- The homepage, GOLA page, `robots.txt`, and `sitemap.xml` returned HTTP 200. The homepage and GOLA page had the expected canonical URLs and no `X-Robots-Tag` exclusion header. The robots file allows crawling and points to the sitemap.
- The live sitemap contained 20 canonical URLs. The withdrawn PDE manuscript remained absent. GOLA remained completed, and the Navier–Stokes project retained no ongoing badge.
- Search lookups did not provide reliable evidence of this domain’s Google indexing state. A search result for another person named Abhyuday Mishra must not be treated as this portfolio or as evidence about its coverage.
- PageSpeed Insights could not run because its API returned a quota-limit response. No Lighthouse, Core Web Vitals, or field performance result is claimed.

## On-page changes

| Item | Earlier rendered build | Updated rendered build |
| --- | --- | --- |
| Longest search title | 77 characters | 60 characters |
| Six note descriptions | 300-character automatic excerpts | Written summaries, 136–149 characters |
| Oculon project description | 240 characters | 142 characters |
| Resume description | 49 characters | 144 characters |
| Homepage main heading | Learning from the structure of things. | Scientific machine learning & quantum computing. |
| Indexable pages | 20 | 20; existing URLs retained |

Character ranges above are editorial budgets, not hard limits imposed by Google. Titles and descriptions remain subject to search engine rewriting.

Every indexable page now has a distinct written description and concise search title. The visible homepage identifies the research fields, and the resume, research, and collection pages have descriptive headings. Existing project and note prose is retained, with section headings added to the longer GOLA, NanoTransformer, and Navier–Stokes pages.

Research pages link directly to the relevant projects. Each of the six notes links to its project, and the qudit project and conference entry link to one another. These links are present in generated HTML and require no JavaScript. Notes show their summaries and author profile links to readers.

The existing Notes publisher previously replaced all front matter during an update. It now preserves authored descriptions, search titles, project relationships, mathematical rendering settings, custom permalinks, and other YAML fields while updating its own title/date/note fields. An integration test covers an update with a renamed note, multiline description, topic list, and stable permalink.

## Validation

The Jekyll build and generated-site audit pass: 22 HTML pages, 20 sitemap URLs, 20 search-index entries, internal links/anchors, JSON-LD, feed XML, and social-card checks. The on-page audit reports no duplicate titles or descriptions, no orphan pages in the main-content link graph, and no article headline mismatches. Ten JavaScript tests and six Python tests pass.

Run the checks locally:

```sh
bundle exec jekyll build
python3 scripts/verify_site.py _site
python3 scripts/verify_seo.py _site --report /tmp/seo-audit.json
python3 -m unittest discover -s tests -p 'test_*.py'
node --test tests/*.test.mjs
```

CI now saves the on-page JSON audit with the workflow run. The audit checks rendered metadata and links; it does not score search rankings, backlinks, keyword demand, or actual inclusion in Google.

## Check actual Google visibility after deployment

Open the existing property in [Google Search Console](https://search.google.com/search-console/). Ownership and inspection results were not available to this audit.

1. Inspect `https://abhyudaymishr.github.io/` and representative project URLs. Compare the live test, indexing verdict, last crawl, any exclusion reason, and Google-selected canonical.
2. Confirm `https://abhyudaymishr.github.io/sitemap.xml` is submitted and successfully processed. A public sitemap does not show whether a Search Console property has submitted it.
3. If an updated page is eligible but not indexed, request indexing after the updated build has deployed. Address the reported exclusion reason if Google gives one.
4. Use the Performance report to follow impressions and clicks for “Abhyuday Mishra”, “GOLA neural operator”, “Oculon hotspot forecasting”, and the project-specific terms. Compare measured results rather than inferring success from HTML checks.

If ownership verification is required, use the code issued for this exact property. `_config.yml` accepts `google_site_verification` and `bing_site_verification`; no code has been invented or inserted. A property already verified through another method does not need a new meta tag.

The updated source remains local until committed and deployed through the existing Pages workflow. No account verification, indexing request, or external profile change was performed.

## Primary references

- [Google SEO Starter Guide](https://developers.google.com/search/docs/fundamentals/seo-starter-guide)
- [Title links in Google Search](https://developers.google.com/search/docs/appearance/title-link)
- [AI features and your website](https://developers.google.com/search/docs/appearance/ai-features)

## Follow-up: name and professional discovery

The homepage now leads with **Abhyuday Mishra**, supported by visible machine learning engineering and quantum computing work. The profile identifies the documented IIT Madras summer research internship and current NFSU studies. Structured data records the actual given name, family name, public GitHub handle, student role, affiliation, and existing professional profile URLs. The resume is also marked as a profile page. This clarifies identity; it does not reserve a search position.

| Search intent | Primary destination | What supports relevance |
| --- | --- | --- |
| Abhyuday Mishra | Homepage | Full name in the title and H1, consistent Person identity, institution and experience |
| Abhyuday Mishra machine learning | Homepage and resume | Visible ML engineering work, project evidence, education and experience |
| Abhyuday Mishra quantum computing | Research and qudit project | Simulation work, collaborative authorship, and conference entry |
| GOLA neural operator / Oculon hotspot forecasting | Respective project pages | Distinct technical descriptions and related research notes |
| Abhyuday / Mishra | Homepage, when relevant to the searcher | These names identify many people; the result order cannot be controlled |
| Machine learning professionals / quantum professional | Profile and research pages, when relevant | Broad competitive queries may seek directories, consultants, employers, or educational material |

After deployment, use Search Console’s Performance report to measure each query’s impressions, clicks, and average position, with country and device filters. Inspect the exact homepage URL if it is not appearing. Confirm that the real GitHub and LinkedIn profiles link back to this portfolio; those external profile changes have not been performed here. Independent references to the actual work are useful evidence of identity and relevance; extra keyword fields cannot replace them.

Google determines indexing, recommendations, and result order. No implementation can guarantee that a particular site will always rank first, including for a full name, and these changes do not make that claim.
