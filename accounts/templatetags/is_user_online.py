from accounts.models import User
from django import template
import online_users.models
register = template.Library()
from datetime import timedelta




@register.simple_tag()
# check if the user online or not
def is_user_online(username):
    """
    register a new template tags called is_user_online
    first you need load the tag bay typing {% load is_user_online %}
    then {% is_user_online username %}
    """
    # get the user object
    get_user = User.objects.get(username=username)
    # get all the users online
    user_status = online_users.models.OnlineUserActivity.get_user_activities(
        timedelta(seconds=60))
    users = (user for user in user_status)
    for user in users:
        # check if the user is online
        if user.user == get_user:
            tailwind = """relative group-hover:bg-green-400 group-hover:border-slate-800 -bottom-4  -mb-5 border-2 bg-green-600 rounded-full"""
            return tailwind