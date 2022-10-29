from django import template
from website.models import Website

register = template.Library()


@register.simple_tag()
def website():
    """
    use this tag to get the website info like title, keywords, description....
    to use this tag:
    first, you should load this tag buy typing {% load website %} type load the_tag_file_name.py
    second, {% website_info  as website_info %}
    and you can you use the tag like an argument {{ website_info.name }} ....
    """
    website = Website.objects.all().first()
    return website