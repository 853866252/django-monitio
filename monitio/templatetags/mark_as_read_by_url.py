# -*- encoding: utf-8 -*-

from django import template
from monitio.models import Monit


register = template.Library()


@register.simple_tag(takes_context=True)
def mark_as_read_by_url(context):
    request = context['request']
    user = request.user
    url = request.get_full_path()
    Monit.objects.filter(user=user, read=False, url=url).update(read=True)
