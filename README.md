Trelloports
===========

Generate reports from Trello boards.

Configuration
=============

You need to provide a YAML configuration file with the following
information:

    trello:
      apikey: <your api key>
      apisecret: <your api secret>
      token: <your oauth token>

    report:
      organization: <your oganization name>
      board: <you board name>

Trelloports will look up board *board* in organization *organization*,
gather up all the lists into a data structure, and pass it to the
jinja2 templating engine.

The default template creates a report in Markdown format (that makes
several assumptions about board names).


