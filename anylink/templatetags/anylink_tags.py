from __future__ import unicode_literals
import re

from django import template

from ..models import AnyLink


register = template.Library()

RTELINK_RE = re.compile(r'<a[^\>]href=["\']#AL(\d+)["\'][^\>]*>')


def rtelink_sub_callback(match):
    try:
        link = AnyLink.objects.get(pk=int(match.group(1)))
    except AnyLink.DoesNotExist:
        # Link not found, to nothing and return the whole string.
        return match.group(0)

    return u'<a href="{0}"{1}{2}{3}>'.format(
        link.get_absolute_url(),
        link.title and ' title="{0}"'.format(link.title) or '',
        link.target and ' target="{0}"'.format(link.target) or '',
        link.css_class and ' class="{0}"'.format(link.css_class) or ''
    )


@register.filter
def insert_anylinks(html):
    return RTELINK_RE.sub(rtelink_sub_callback, html)
