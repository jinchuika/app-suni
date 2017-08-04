from django import template
from django.utils.html import format_html


register = template.Library()


@register.simple_tag(name='editable_field')
def editable_field(value, name, pk, url, editable=True, *args, **kwargs):
    if not editable:
        return value
    data_type = kwargs.get('data_type', 'text')
    source_list = kwargs.get('source_list', None)
    source_id = kwargs.get('source_id', None)
    source_text = kwargs.get('source_text', None)
    if source_list and source_id and source_text:
        source = '['
        source += ', '.join('{{ \'{}\': \'{}\' }}'.format(item[source_id], item[source_text]) for item in source_list.values())
        source += ']'
    else:
        source = ''
    return format_html(
        '<a href="#" class="editable" data-name="{name}" data-type="{data_type}" data-pk="{pk}" data-url="{url}" data-source="{source}">{value}</a>',
        name=name,
        data_type=data_type,
        pk=pk,
        url=url,
        value=value,
        source=source)
