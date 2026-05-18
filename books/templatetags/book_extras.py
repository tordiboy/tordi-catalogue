from django import template

register = template.Library()

@register.filter
def get_item(access_map, key):
    return access_map.get(key, False)