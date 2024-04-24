from django import template
register = template.Library()

# This is necessary to get pagination to work properly
# Without it, the range of pages would be the entire database

@register.filter
def get_pagination_range(value, arg):
    start, end = map(int, arg.split(','))
    return range(start, end + 1)