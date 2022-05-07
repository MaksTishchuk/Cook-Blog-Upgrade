from django import template
from ..models import Photo, Gallery

register = template.Library()


@register.inclusion_tag('blog/include/tags/gallery_tag.html')
def get_gallery():
    galleries = Gallery.objects.all()
    return {"galleries": galleries}
