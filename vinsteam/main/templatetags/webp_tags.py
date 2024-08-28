import base64
from io import BytesIO

from django import template
from django.utils.safestring import mark_safe
from PIL import Image

register = template.Library()


@register.simple_tag
def webp_thumbnail(image, width, quality=85):
    img = Image.open(image.path)
    original_width, original_height = img.size
    height = int(width / original_width * original_height)
    size = (width, height)
    img.thumbnail(size)
    webp_image = img.convert("RGB")
    
    # Создание объекта BytesIO для временного хранения данных
    buffer = BytesIO()
    
    # Сохранение изображения в формате WebP в буфер
    webp_image.save(buffer, format="WEBP", quality=quality)
    
    # Получение данных из буфера и кодирование их в строку base64
    webp_data = base64.b64encode(buffer.getvalue()).decode()
    
    return mark_safe(f"data:image/webp;base64,{webp_data}")


@register.simple_tag
def endwebp_thumbnail():
    pass
