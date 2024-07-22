from wagtail.admin.panels import FieldPanel

from .common import SimpleModel


class Account(SimpleModel):
    panels = [
        FieldPanel("name"),
    ]

    class Meta:
        ordering = ["name"]
        verbose_name = "Счёт"
        verbose_name_plural = "Счета"
