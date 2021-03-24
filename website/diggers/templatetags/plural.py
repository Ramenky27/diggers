from django import template

register = template.Library()


@register.filter
def plural(value, arg=''):
    forms = arg.split(',')

    if value == 1:
        return forms[0]
    elif value == 2:
        return forms[1]
    else:
        return forms[2]
