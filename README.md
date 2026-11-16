# Abhyuday Mishra — research portfolio

A static Jekyll site for scientific machine learning, quantum computing, and topology. The visual direction takes cues from Google DeepMind’s spacious research pages; the identity, content, and mathematical artwork are original to this portfolio.

## Local development

Use a supported Ruby installation with Bundler, Node 22 or newer, and Python 3.

```sh
bundle install
bundle exec jekyll serve --host 127.0.0.1
```

The site serves at `http://127.0.0.1:4000`. Important content and navigation work without JavaScript. Search and project filtering enhance the rendered pages.

## Architecture

| Concern | Location | Responsibility |
| --- | --- | --- |
| Content and configuration | `_projects/`, `_publications/`, `_posts/`, `_data/`, `_config.yml` | Research text, authorship, publication status, navigation, home copy, project categories |
| Presentation | `_layouts/`, `_includes/`, `assets/css/` | Page composition, accessible controls, article structure, responsive visual design |
| Content rules | `assets/js/core/content.mjs` | Search ranking, normalization, filtering, same-origin link validation; no browser dependencies |
| Data access | `assets/js/data/content-repository.mjs` | A lazy, shared content-index request, caching, validation, retry after failures |
| Browser adapters | `assets/js/ui/` | DOM updates, form/dialog behavior, filters and URL state |
| Composition | `assets/js/app.mjs` | Wires the data boundary and UI adapters together |
| Publishing utilities | `scripts/publish_note.py`, `scripts/publish.sh` | Existing authoring workflow, separate from the site interface |

Project `featured`, `order`, `cover`, `short_title`, `card_summary`, and `category` fields control the project cards. Edit `_data/home.yml` for the home-page copy. Full article titles and existing URLs are retained. Publication `author_list` is the structured equivalent of visible `authors`; keep them in sync. The category buttons are generated from project `category` values, so adding a research area requires no JavaScript or template change.

## Search and AI discovery

- Every important page is pre-rendered HTML with a stable canonical URL, descriptive metadata, semantic landmarks, and crawlable links.
- JSON-LD connects the researcher, website, pages, breadcrumbs, and creative works. Conference papers and drafts preserve their actual status and authorship. Do not add unverified metrics, publication dates, or affiliations.
- `sitemap.xml`, `feed.xml`, `content-index.json`, `llms.txt`, and `llms-full.txt` are generated from the same Jekyll collections as the visible pages. No manual content-index synchronization is needed.
- The JSON index contains canonical URLs, titles, topics, status, descriptions, and article source text. It supports on-site search and read-only retrieval by external tools. It is not a live MCP or agent execution server.
- The `llms` files are optional reading aids for tools that support them. Google does not require them for AI search. Indexability, useful content, internal links, and performance remain the foundation; rankings and inclusion cannot be guaranteed.
- Search results and the 404 page are `noindex` and excluded from the sitemap and content index. Development scripts and tests are excluded from the published artifact. Modification dates are only emitted when present in content, not fabricated at build time.
- Social previews use the committed 1200 × 630 PNG; original SVG visuals use no remote image dependencies on the home page. MathJax loads only for content with `math: true`.

Submit `https://abhyudaymishr.github.io/sitemap.xml` in the owner’s Google Search Console and Bing Webmaster Tools to monitor indexing after deployment. These account operations are not performed by this repository.

## Validation and deployment

```sh
node --test tests/*.test.mjs
bundle exec jekyll build
python3 scripts/verify_site.py _site
```

CI runs the same checks before uploading the GitHub Pages artifact. Pull requests validate without deploying; pushes to `main` publish through the existing Pages deployment. The output audit checks canonical URLs, titles/descriptions, one main heading and landmark per page, image dimensions, local links and anchors, JSON-LD parsing, sitemap/index coverage, feed XML, and social-card dimensions. It is not a substitute for browser accessibility, mobile-layout, or real-world performance testing.

Rebuild the original decorative mathematical SVGs with `python3 scripts/generate_visuals.py`. Install Pillow in your Python environment to regenerate the matching PNG social card; otherwise the committed PNG is retained. Illustrations are conceptual artwork, not experiment results.
