from django import template
register = template.Library()

@register.filter
def get_pagination_range(value, arg):
    start, end = map(int, arg.split(','))
    return range(start, end + 1)