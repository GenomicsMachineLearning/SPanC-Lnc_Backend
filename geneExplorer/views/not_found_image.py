import os
import base64
import django.conf as django_conf


class NotFoundImage:
    png_path = os.path.join(django_conf.settings.BASE_DIR, 'static/no_data.png')
    _base64_png = None

    @staticmethod
    def not_found():
        if NotFoundImage._base64_png is None:
            try:
                with open(NotFoundImage.png_path, 'rb') as png_file:
                    png_data = png_file.read()
                    NotFoundImage._base64_png = base64.b64encode(png_data).decode('utf-8')
            except FileNotFoundError:
                return None
        return NotFoundImage._base64_png
