from core.models import Topic
from django import template

register = template.Library()
"""
    register a new template tags called is_joined_user
    first you need load the tag bay typing {% load join_quit_topic %}
    then {% join_quit_topic topic request %}
    """


@register.simple_tag
def join_quit_topic(topic, request):
    get_topic = Topic.objects.get(name=topic.name)
    is_joined = get_topic.is_user_joined(request)
    if is_joined:
        return 'Quit'
    else:
        return 'Join'
