Academic Computing Projects ({{date}})
======================================================================

In progress
===========

---
These are the projects that team members are either currently
working on or expect to be working on over the next few weeks.
---

{% for card in report['In Progress'] %}
{% include "card.md" %}
{% endfor %}

Recently completed
==================

---
These are projects that have recently been completed.
---

{% for card in report['Done'] %}
{% include "card.md" %}
{% endfor %}

Future projects
===============

---
These are projects that have been identified but that may not see
active progress over the next few weeks.
---

{% for card in report['To Do'] %}
{% include "card.md" %}
{% endfor %}

