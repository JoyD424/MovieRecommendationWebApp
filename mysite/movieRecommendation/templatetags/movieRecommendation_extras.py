from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter()
# Inclusive range starting at 1
def tags_range(min):
    return range(1, min + 1)