import bleach

from urllib.parse import urlparse
from django import template
from django.conf import settings

from django.utils.safestring import mark_safe
from django_bleach.utils import get_bleach_default_options

register = template.Library()
bleach_args = get_bleach_default_options()


def check_src(tag, name, value):
    if tag == 'iframe':
        if name == 'src':
            p = urlparse(value)
            return p.netloc in getattr(settings, 'BLEACH_ALLOWED_IFRAME_SRC', [])
    else:
        return name in getattr(settings, 'BLEACH_ALLOWED_ATTRIBUTES', [])


@register.filter(name='bleach')
def bleach_value(value, tags=None):
    if value is None:
        return None

    if tags is not None:
        args = bleach_args.copy()
        args['tags'] = tags.split(',')
    else:
        args = bleach_args

    args['attributes'] = check_src
    bleached_value = bleach.clean(value, **args)
    return mark_safe(bleached_value)
