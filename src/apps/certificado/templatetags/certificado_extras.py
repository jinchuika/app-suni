from django import template

register = template.Library()

@register.filter(name='to_number')
def to_number(value): 
    return int(value)