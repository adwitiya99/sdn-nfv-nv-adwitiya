from django import template
import json

register = template.Library()


@register.filter
def toListFromJSON(value):
    try:
        return json.loads(value)
    except:
        return []
