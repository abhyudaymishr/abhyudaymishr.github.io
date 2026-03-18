---
title: Blog
permalink: /blog/
kicker: Notes
intro: "Technical notes and philosophical research essays on operator learning, quantum systems, topology, and model-building."
---
<div class="cards">
  {% for post in site.posts %}
    <a class="card-link" href="{{ post.url | relative_url }}">
      <strong>{{ post.title }}</strong>
      <span>{{ post.date | date: "%B %-d, %Y" }}</span>
    </a>
  {% endfor %}
</div>
