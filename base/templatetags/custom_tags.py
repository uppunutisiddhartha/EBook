# base/templatetags/custom_tags.py
from django import template

register = template.Library()

@register.filter
def to(value, arg):
    """
    Generates a range from 'value' to 'arg' inclusive.
    Usage: {% for i in 1|to:5 %}
    """
    try:
        start = int(value)
        end = int(arg)
        return range(start, end + 1)
    except (ValueError, TypeError):
        return []
