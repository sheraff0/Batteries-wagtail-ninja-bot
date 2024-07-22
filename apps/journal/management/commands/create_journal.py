import os

from django.core.management.base import BaseCommand, CommandError

from apps.root.models import Home
from apps.journal.models import Journal
from apps.assets import journal_data
from contrib.wagtail.services import get_or_create_page


class Command(
    BaseCommand
):

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **kwargs):
        self.set_home_page()
        self.create_journal()

    def set_home_page(self):
        self.home_page = Home.objects.live().first()

    def create_journal(self):
        get_or_create_page(Journal, parent=self.home_page, **journal_data)
