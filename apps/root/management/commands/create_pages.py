import os

from django.core.management.base import BaseCommand, CommandError

from wagtail.models import Page, Site
from wagtail.images import get_image_model

from contrib.utils.files import get_or_create_file_object
from apps.root.models import (
    Home, HomeSlide, HomeCategory,
    Country,
    Contacts,
)
from apps.assets import home_data, contacts_data
from apps.root.services import CreatePagesMethods
from .sets import select_option_input

BASE_URL_OPTIONS = (
    ('127.0.0.1', 8004),
    ('акб-анапа.рф', 443),
)


class Command(
    CreatePagesMethods,
    BaseCommand
):

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **kwargs):
        self.set_base_url()
        self.create_home_page()
        self.create_contacts()

    def set_base_url(self):
        self.base_url = select_option_input(
            BASE_URL_OPTIONS, "URL сайта")

    def clear_tree(self):
        Page.objects.filter(depth__gt=1).delete()

    def create_home_page(self):
        host, port = self.base_url
        #self.clear_tree()
        root = Page.get_first_root_node()
        self.home_page = Home.objects.first()
        _data = self.get_data(home_data)
        slides, categories = map(_data.pop, ("slides", "categories"))
        if not self.home_page:
            self.home_page = Home(**_data)
            root.add_child(instance=self.home_page)
            Site.objects.create(
                hostname=host,
                port=port,
                root_page=self.home_page,
                is_default_site=True,
                site_name=host
            )
        self.create_home_slides(slides)
        self.create_home_categories(categories)

    def create_home_slides(self, slides):
        self.create_related(HomeSlide, self.home_page, slides)

    def create_home_categories(self, categories):
        self.create_related(HomeCategory, self.home_page, categories)

    def create_contacts(self):
        self.contacts = self.create_page(Contacts, **contacts_data)
