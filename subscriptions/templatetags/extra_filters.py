from django import template
from django.contrib.auth.models import Group
from subscriptions.models import Subscriber


register = template.Library()


@register.filter(name='in_group')
def in_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False


@register.filter(name='is_active')
def is_active(user, model_name):
    record = Subscriber.objects.filter(user=user)[0]
    return True if record.active else False
