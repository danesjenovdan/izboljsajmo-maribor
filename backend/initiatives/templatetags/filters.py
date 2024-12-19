from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
def get_class(value):
    return value.__class__.__name__.lower()
