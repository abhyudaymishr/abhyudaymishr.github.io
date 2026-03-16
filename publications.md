---
title: Publications
permalink: /publications/
kicker: Writing
intro: "Draft manuscripts, research notes, and publication-ready work in progress."
---
{% assign ordered_publications = site.publications | sort: "year" | reverse %}
<div class="publication-list">
  {% for publication in ordered_publications %}
    <article class="publication-card">
      <p class="eyebrow">{{ publication.type | default: "Writing" }}</p>
      <h2 class="publication-card__title">{{ publication.title }}</h2>
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
  Replace draft entries with accepted papers, arXiv links, citation blocks, and code/data links as the work matures.
</div>
