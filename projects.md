---
title: Projects
permalink: /projects/
kicker: Research & engineering
intro: "From mathematical ideas to working systems. Explore experiments in scientific machine learning, quantum computing, topology, and language modeling."
wide: true
collection_page: true
---
<div data-project-browser>
  <div class="filter-bar" role="group" aria-label="Filter projects by research area" data-project-filters hidden>
    <button class="filter-button" type="button" data-filter="all" aria-pressed="true">All research</button>
    {% assign categories = site.projects | sort: 'order' | map: 'category' | uniq %}
    {% for category in categories %}<button class="filter-button" type="button" data-filter="{{ category | escape }}" aria-pressed="false">{{ category }}</button>{% endfor %}
  </div>
  <p class="filter-count" role="status" data-project-count hidden></p>
  <div class="project-grid">
    {% assign ordered_projects = site.projects | sort: 'order' %}
    {% for project in ordered_projects %}{% include project-card.html project=project %}{% endfor %}
  </div>
</div>
