import json

from django import template
from django.utils.html import mark_safe

register = template.Library()


@register.simple_tag
def many_to_many_uuid_to_string(values):
    values_in_json = json.dumps([str(value) for value in values])
    return mark_safe(values_in_json)
