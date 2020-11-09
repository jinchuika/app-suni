import json

from django import template


register = template.Library()


@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()

@register.filter(name='load_json')
def load_json(data):
	print("Entro")
	return json.loads(data)
