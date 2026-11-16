---
last_modified_at: "2026-11-16"
description: "Conference work by Abhyuday Mishra and collaborators on high-performance qudit simulation, with authorship, venue, and project context."
seo_title: "Qudit Simulation Publications | Abhyuday Mishra"
title: "Quantum computing publications"
permalink: /publications/
wide: true
collection_page: true
kicker: Conference research
intro: "Collaborative conference work in high-performance qudit simulation, with authorship and venue details."
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
        <a class="button button--primary" href="{{ publication.url | relative_url }}">Read publication details</a>
      </div>
    </article>
  {% endfor %}
</div>

<div class="note-block">
  Authorship and conference details are stated in each entry. Explore the <a href="{{ '/projects/qudit-circuit-framework/' | relative_url }}">related qudit quantum circuit framework</a> for implementation context.
</div>
