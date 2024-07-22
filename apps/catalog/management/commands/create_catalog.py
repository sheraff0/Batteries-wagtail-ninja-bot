from django.core.management.base import BaseCommand, CommandError

from apps.assets import catalog_data
from apps.catalog.services import CreateCatalog


class Command(
    BaseCommand
):

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **kwargs):
        CreateCatalog(catalog_data)()
