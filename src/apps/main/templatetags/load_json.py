import json

from django import template

register = template.Library()

@register.filter(name='load_json')
def load_json(data):
    return json.loads(data)