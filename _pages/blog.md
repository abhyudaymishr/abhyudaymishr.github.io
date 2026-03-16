---
title: Blog
permalink: /blog/
kicker: Notes
intro: "Short research essays on operator theory, sparse attention, and quantum abstractions."
---
<div class="cards">
  {% for post in site.posts %}
    <a class="card-link" href="{{ post.url | relative_url }}">
      <strong>{{ post.title }}</strong>
      <span>{{ post.date | date: "%B %-d, %Y" }}</span>
    </a>
  {% endfor %}
</div>

