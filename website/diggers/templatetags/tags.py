from django import template
from taggit.models import TaggedItem, Tag

register = template.Library()


@register.simple_tag
def tags(entity='post'):
    tag_ids = TaggedItem.objects.filter(content_type__model=entity.lower()).values_list('tag_id', flat=True)
    queryset = Tag.objects.filter(id__in=tag_ids)

    return queryset
