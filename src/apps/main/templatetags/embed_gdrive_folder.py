import re
from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def embed_gdrive_folder(url, mode='grid'):
    try:
        found = re.search('((?<=(id|ID)/)|(?<=(\?|\&)id=)|(?<=folders/))([\w-]+)', url).group()
    except AttributeError:
        # AAA, ZZZ not found in the original string
        found = ''
    remote_url = 'https://drive.google.com/embeddedfolderview?id={}'.format(found)
    link_text = '<small><a href="{url}" target="_blank">Link</a></small>'.format(url=url)
    return '<iframe src="{remote_url}#{mode}" style="width:100%; height:400px; border:0;"></iframe>{link_text}'.format(
        remote_url=remote_url, mode=mode, link_text=link_text)
