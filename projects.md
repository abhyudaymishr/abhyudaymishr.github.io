---
title: Projects
permalink: /projects/
kicker: Build
intro: "Research systems and prototypes spanning operator learning, quantum circuits, topology, and efficient ML, each paired with a reflective research note."
---
{% assign ordered_projects = site.projects | sort: "order" %}
<div class="cards">
  {% for project in ordered_projects %}
    <a class="project-card" href="{{ project.url | relative_url }}">
      {% if project.image %}
        <div class="project-card__media">
          <img src="{{ project.image }}" alt="{{ project.image_alt | default: project.title }}">
        </div>
      {% else %}
        <div class="project-card__media project-card__media--fallback">
          <span>{{ project.topics | first | default: "Research" }}</span>
        </div>
      {% endif %}
      <div class="project-card__body">
        <p class="eyebrow">{{ project.topics | first | default: "Research" }}</p>
        <strong>{{ project.title }}</strong>
        <span>{{ project.summary }}</span>
      </div>
    </a>
  {% endfor %}
</div>
