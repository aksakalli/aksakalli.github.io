{% extends 'markdown.tpl' %}

{%- block header -%}
---
layout: post
title: "{{resources['metadata']['name'] | userfriendly_title }}"
shorttitle: "{{nb['metadata']['shorttitle']}}"
tags:
    - python
    - notebook
---
{%- endblock header -%}

{% block in_prompt %}
<!-- **In [{{ cell.execution_count }}]:** -->
{% endblock in_prompt %}

{% block input %}
{{ '{% highlight python %}' }}
{{ cell.source }}
{{ '{% endhighlight %}' }}
{% endblock input %}

{% block data_svg %}
![svg]({{ output.metadata.filenames['image/svg+xml'] | path2support }})
{% endblock data_svg %}

{% block data_png %}
![png]({{ output.metadata.filenames['image/png'] | path2support }})
{% endblock data_png %}

{% block data_jpg %}
![jpeg]({{ output.metadata.filenames['image/jpeg'] | path2support }})
{% endblock data_jpg %}

{% block markdowncell scoped %}
{{ cell.source | wrap_text(80) | markdown_changes }}
{% endblock markdowncell %}

{% block headingcell scoped %}
{{ '#' * cell.level }} {{ cell.source | replace('\n', ' ') }}
{% endblock headingcell %}

{%- block footer -%}
<p>
  <a type="button" href="/notebooks/{{resources['metadata']['name']}}.ipynb" class="btn btn-secondary btn-lg btn-block">Download the Notebook</a>
</p>
{%- endblock footer -%}
