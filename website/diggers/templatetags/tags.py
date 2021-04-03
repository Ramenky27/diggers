import math
from django import template
from taggit.models import Tag
from django.db.models import Count, Min, Max

register = template.Library()


class TagCloud(object):
    tags = None
    queryset = None
    max_weight = 0
    min_weight = 0

    def __init__(self, steps=6, min_count=1, hidden=False):
        self.steps = steps
        self.hidden = hidden
        self.min_count = min_count
        self.set_tags()
        if len(self.tags):
            self.find_min_max()
            self.thresholds = self.calculate_thresholds()

    def set_tags(self):
        query = {
            'taggit_taggeditem_items__content_type__app_label': 'diggers',
        }
        if not self.hidden:
            query['postabstract__is_hidden'] = False

        queryset = Tag.objects.filter(**query).distinct()\
            .annotate(count=Count('taggit_taggeditem_items')).order_by('name')

        self.queryset = queryset
        self.tags = queryset.values('name', 'slug', 'count')

    def find_min_max(self):
        edges = self.queryset.aggregate(max=Max('count'), min=Min('count'))
        self.max_weight = edges['max']
        self.min_weight = edges['min']

    def calculate_thresholds(self):
        delta = (self.max_weight - self.min_weight) / float(self.steps)
        return [self.min_weight + i * delta for i in range(1, self.steps + 1)]

    def calculate_tag_weight(self, weight):
        """
        Logarithmic tag weight calculation is based on code from the
        `Tag Cloud`_ plugin for Mephisto, by Sven Fuchs.

        .. _`Tag Cloud`: http://www.artweb-design.de/projects/mephisto-plugin-tag-cloud
        """
        if self.max_weight == 1:
            return weight
        else:
            # Fuchs-method
            return math.log(weight) * self.max_weight / math.log(self.max_weight)

    def calculate_cloud(self):
        tags_list = []
        if len(self.tags):
            for tag in self.tags:
                font_set = False
                tag_weight = self.calculate_tag_weight(tag['count'])
                for i in range(self.steps):
                    if not font_set and tag_weight <= self.thresholds[i]:
                        tag['level'] = i + 1
                        font_set = True
                tags_list.append(tag)
        return tags_list


@register.simple_tag(takes_context=True)
def tags(context):
    return TagCloud(hidden=context.request.user.has_perm('diggers.hidden_access')).calculate_cloud()
