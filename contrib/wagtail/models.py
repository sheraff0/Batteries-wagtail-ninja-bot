import re
from unidecode import unidecode

from django.utils.html import format_html

from wagtail.models import Page as PageBase


class UnidecodeMixin:
    def _get_autogenerated_slug(self, base_slug):
        _res = super()._get_autogenerated_slug(base_slug)
        _res = unidecode(_res)
        _res = re.sub(r"[^\w\d-]", "", _res)
        return _res


class Page(UnidecodeMixin, PageBase):
    class Meta:
        abstract = True


class IconImgMixin:
    @property
    def icon_img(self):
        try: return f'<img src="{self.icon.file.url}" style="max-height: 1.5rem; margin-bottom: -0.3rem"/>'
        except: return ""

    def get_admin_display_title(self):
        return format_html(f"{self.icon_img}&nbsp;{self.title}")