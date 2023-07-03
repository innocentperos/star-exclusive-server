from django import template

register = template.Library()

@register.filter
def get(d, key):
    return dict(d).get(key, '')


@register.filter
def uppercase(value):
    return value.upper()