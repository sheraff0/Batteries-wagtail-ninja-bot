from unidecode import unidecode

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from apps.root.models import Home, Contacts
from apps.catalog.models import Catalog, Category, Product


superuser_data = dict(
    username="akb-anapa",
    email="roma2910@list.ru",
    is_staff=True,
    is_superuser=True,
)


class Command(
    BaseCommand
):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **kwargs):
        self.unidecode_slugs()

    @staticmethod
    def unidecode_slugs():
        for Model in [Home, Catalog, Catalog, Product, Contacts]:
            for page in Model.objects.live():
                _slug = page.slug
                _decoded = unidecode(_slug)
                if _slug != _decoded:
                    page.slug = None
                    page.save()
