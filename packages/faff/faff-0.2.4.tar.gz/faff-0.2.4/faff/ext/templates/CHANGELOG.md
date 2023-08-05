# {{ title }}

{% for audience in audiences -%}
{% if audience.name %}## {{ audience.name }}{% endif %}

{% for tag in audience.tags -%}
{% if tag.name %}### [{{ tag.name }}]{% if tag.date %} - {{ tag.date }}{% endif %}{% endif %}

{% for category in tag.categories -%}
{% if category.name %}#### {{ category.name }}{% endif %}

{% for commit in category.commits -%}
{% if commit.subject %}-   {{ commit.subject }}{% if commit.author %} [{{ commit.author }}]{% endif %}{% endif %}
{% endfor %}
{% endfor %}
{% endfor %}
{% endfor %}
