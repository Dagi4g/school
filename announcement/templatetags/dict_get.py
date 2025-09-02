from django import template

register = template.Library()

@register.filter
def dict_get(d, key):
    return d.get(key) if d else None

@register.filter
def dict_item(d):
    return d.items() if d else []