from copy import deepcopy

from wagtail.images import get_image_model

from apps.assets import ASSETS_PATH
from apps.root.models import (
    Country,
)
from contrib.utils.files import get_or_create_file_object
from contrib.wagtail.pages import get_or_create_page

IMAGES_PATH = ASSETS_PATH / "img"


class CreatePagesMethods:
    def create_page(self, Model=None, title=None, parent=None, **kwargs):
        kwargs["seo_title"] = title
        return get_or_create_page(Model=Model, title=title, parent=parent or self.home_page, **kwargs)

    def create_related(self, Model, parent, data):
        for i, item in enumerate(data):
            _data = self.get_data(item)
            _title = _data.pop("title")
            Model.objects.update_or_create(page=parent, title=_title, defaults=dict(
                sort_order=i, **_data))

    def get_file(self, Model, path, image_name):
        return get_or_create_file_object(Model, path, image_name)

    def get_country(self, name):
        if name:
            country, _ = Country.objects.get_or_create(name=name)
            return country

    def link_objects(self, data):
        Image = get_image_model()
        for k, v in data.items():
            if "image" in k:
                v = self.get_file(Image, IMAGES_PATH, v)
            if k == "country":
                v = self.get_country(v)
            if k in ["published", "calcium", "low", "efb", "agm", "silver"]:
                v = bool(v)
            data[k] = v
        return data

    def get_data(self, data):
        _data = deepcopy(data)
        self.link_objects(_data)
        return _data
