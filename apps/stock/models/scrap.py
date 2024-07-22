from django.db import models

from wagtail.admin.panels import FieldPanel, FieldRowPanel

SCRAP_PRICE_DEFAULT = 62


class ScrapPrice(models.Model):
    date_from = models.DateField("Начиная с...")
    price = models.IntegerField("Цена")

    panels = [
        FieldRowPanel([
            *map(FieldPanel, ("date_from", "price"))
        ])
    ]

    def __str__(self):
        return f"{self.price} руб./кг (c {self.date_from})"

    class Meta:
        ordering = ["date_from"]
        verbose_name = "Цена лома"
        verbose_name_plural = "Цены лома"
