from copy import deepcopy

from apps.root.models import Home
from apps.root.services import CreatePagesMethods
from apps.catalog.models import (
    Catalog, Category, Product,
)


class CreateCatalog(CreatePagesMethods):
    def __init__(self, data):
        self.data = data

    def set_home_page(self):
        self.home_page = Home.objects.first()

    def create_catalog(self):
        _data = deepcopy(self.data)
        _products = _data.pop("products")
        self.catalog = self.create_page(Catalog, **_data)
        for product in _products:
            _path = product.pop("path")
            _category = self.create_category_path(_path, self.catalog)
            product["image"] = "products/" + product["image"] if product["image"] else None
            self.create_product(product, _category)

    def create_category_path(self, path, parent):
        for title in path.split("/"):
            parent = self.create_category(title, parent)
        return parent

    def create_category(self, title, parent):
        return self.create_page(Category, title=title, parent=parent)

    def create_product(self, data, parent):
        _data = self.get_data(data)
        print(_data)
        self.create_page(Product, parent=parent, **_data)

    def __call__(self, *args, **kwargs):
        self.set_home_page()
        self.create_catalog()
