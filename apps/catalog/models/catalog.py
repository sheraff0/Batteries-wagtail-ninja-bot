from django.db import models

from wagtail.admin.panels import HelpPanel

from contrib.wagtail.models import Page
from apps.root.models.mixins import CommonPagesMixin
from .mixins import CatalogProductsMixin, CatalogNavigationMixin


class Catalog(CatalogNavigationMixin, CatalogProductsMixin, CommonPagesMixin, Page):
    parent_page_types = ["root.Home"]
    subpage_types = ["Category"]

    max_count = 1

    @property
    def products(self):
        return self.get_products()

    class Meta:
        verbose_name = "Каталог"


class Category(CatalogNavigationMixin, CatalogProductsMixin, CommonPagesMixin, Page):
    parent_page_types = ["Catalog", "Category"]
    subpage_types = ["Category", "Product"]

    class Meta:
        verbose_name = "Категория"
