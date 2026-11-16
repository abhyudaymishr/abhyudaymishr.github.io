---
title: Publications
permalink: /publications/
wide: true
collection_page: true
kicker: Papers & manuscripts
intro: "Conference work and manuscripts, with authorship and publication status stated for each entry."
---
{% assign ordered_publications = site.publications | sort: "year" | reverse %}
<div class="publication-list">
  {% for publication in ordered_publications %}
    <article class="publication-card">
      <p class="eyebrow">{{ publication.type | default: "Writing" }}</p>
      <h2 class="publication-card__title"><a href="{{ publication.url | relative_url }}">{{ publication.title }}</a></h2>
      <p class="publication-card__meta">
        {{ publication.authors }}
        {% if publication.venue %}<span class="meta-separator">/</span>{{ publication.venue }}{% endif %}
        {% if publication.year %}<span class="meta-separator">/</span>{{ publication.year }}{% endif %}
      </p>
      {% if publication.abstract %}
        <p class="publication-card__abstract">{{ publication.abstract }}</p>
      {% endif %}
      <div class="tag-grid tag-grid--left">
        {% for keyword in publication.keywords %}
          <span class="chip">{{ keyword }}</span>
        {% endfor %}
      </div>
      <div class="publication-card__actions">
        <a class="button button--primary" href="{{ publication.url | relative_url }}">Open Entry</a>
      </div>
    </article>
  {% endfor %}
</div>

<div class="note-block">
  Manuscripts in preparation are listed as drafts. Conference work and draft research are identified separately in each entry.
</div>
