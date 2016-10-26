from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def telefonica(empresa):
    if empresa == "claro":
        return "red"
    elif empresa == "tigo":
        return "blue"
    elif empresa == "movistar":
        return "green"
    else:
        return "yellow"
