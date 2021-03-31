from django import template
from django.db.models import Count
from ..models import Category

register = template.Library()


@register.simple_tag
def categories():
    queryset = Category.objects.annotate(posts_count=Count('postabstract')).all()

    return queryset
