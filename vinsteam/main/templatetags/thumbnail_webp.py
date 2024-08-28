import io

from django import template
from PIL import Image

register = template.Library()

@register.simple_tag
def thumbnail_webp(image_file, width):
    im = Image.open(image_file)
    im.thumbnail((width, width))
    im_io = io.BytesIO()
    im.save(im_io, 'WEBP')
    im_data = im_io.getvalue()
    return im_data
