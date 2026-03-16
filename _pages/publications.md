---
title: Publications
permalink: /publications/
kicker: Writing
intro: "Draft manuscripts, research notes, and publication-ready work in progress."
---
{% assign ordered_publications = site.publications | sort: "year" | reverse %}
<div class="cards">
  {% for publication in ordered_publications %}
    <a class="card-link" href="{{ publication.url | relative_url }}">
      <strong>{{ publication.title }}</strong>
      <span>{{ publication.venue }}{% if publication.year %} / {{ publication.year }}{% endif %}</span>
    </a>
  {% endfor %}
</div>

<p class="muted">Replace draft entries with accepted papers, preprints, links, and citation metadata as your list matures.</p>

