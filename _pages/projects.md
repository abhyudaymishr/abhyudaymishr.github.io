---
title: Projects
permalink: /projects/
kicker: Build
intro: "Research systems and prototypes spanning operator learning, quantum circuits, and ML infrastructure."
---
{% assign ordered_projects = site.projects | sort: "order" %}
<div class="cards">
  {% for project in ordered_projects %}
    <a class="card-link" href="{{ project.url | relative_url }}">
      <strong>{{ project.title }}</strong>
      <span>{{ project.summary }}</span>
    </a>
  {% endfor %}
</div>

