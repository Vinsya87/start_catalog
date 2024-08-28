import os

from django.core.files.storage import FileSystemStorage
from PIL import Image


def favicon_upload_to(instance, filename):
    return f'favicons/{filename}'

def process_favicon(instance):
    input_path = instance.favicon.path
    output_path = os.path.join(os.path.dirname(input_path))

    sizes = [16, 24, 32, 48, 64, 76, 96, 120, 144, 152, 167, 180, 192, 512]

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    with Image.open(input_path) as img:
        for size in sizes:
            resized_img = img.resize((size, size), Image.LANCZOS)
            output_filename = f"favicon_{size}x{size}.png"
            resized_img.save(os.path.join(output_path, output_filename))

        sizes_to_convert = [16, 24, 32]
        for size in sizes_to_convert:
            resized_img = img.resize((size, size), Image.LANCZOS)
            output_filename = f"favicon_{size}x{size}.ico"
            resized_img.save(os.path.join(output_path, output_filename), format="ICO")
