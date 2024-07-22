from django.db import models

from wagtail.admin.panels import FieldPanel, MultiFieldPanel

from contrib.wagtail.models import Page
from .mixins import CommonPagesMixin


class Contacts(CommonPagesMixin, Page):
    name = models.CharField("Наименование", max_length=128, null=True, blank=True)
    # Social
    avito = models.CharField("Avito", max_length=128, null=True, blank=True)
    whatsapp = models.CharField("WhatsApp", max_length=128, null=True, blank=True)
    telegram = models.CharField("Telegram", max_length=128, null=True, blank=True)
    # Contacts
    email = models.CharField("Email", max_length=32, null=True, blank=True)
    phone = models.CharField("Телефон", max_length=32, null=True, blank=True)
    schedule = models.TextField("Часы работы", null=True, blank=True)
    # Location
    address = models.CharField("Адрес", max_length=64, null=True, blank=True)
    maps_url = models.CharField("Ссылка на карты", max_length=64, null=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("name"),
        MultiFieldPanel([
            *map(FieldPanel, ("email", "phone", "schedule")),
        ], heading="Контакты"),
        MultiFieldPanel([
            *map(FieldPanel, ("avito", "whatsapp", "telegram")),
        ], heading="Социальные сети"),
        MultiFieldPanel([
            *map(FieldPanel, ("address", "maps_url")),
        ], heading="Местоположение"),
    ]

    parent_page_types = ["Home"]
    subpage_types = []

    max_count = 1
