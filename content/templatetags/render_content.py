from content.models import Contents
from django import template
register = template.Library()

@register.inclusion_tag('snippets/render_content.html')
def render_content(content_obj):
    if isinstance(content_obj,Contents):
        #use a try block here?
        chapter_content = content_obj.lecture.url
       
        return {'chapter_content':chapter_content}


