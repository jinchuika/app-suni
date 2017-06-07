import re
from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def embed_gdrive_folder(url):
    try:
        found = re.search('((?<=(id|ID)/)|(?<=(\?|\&)id=)|(?<=folders/))([\w-]+)', url).group()
    except AttributeError:
        # AAA, ZZZ not found in the original string
        found = ''
    return '<iframe src="https://drive.google.com/embeddedfolderview?id={}#grid" style="width:100%; height:500px; border:0;"></iframe>'.format(
        found)
