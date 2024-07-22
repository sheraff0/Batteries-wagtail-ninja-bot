from django.db import models
from modelcluster.fields import ParentalKey

from wagtail.admin.panels import FieldPanel, FieldRowPanel
from wagtail.models import Orderable


class SalePayment(Orderable):
    sale = ParentalKey("sales.Sale", on_delete=models.CASCADE,
        related_name="payments", verbose_name="Продажа")
    date = models.DateField("Дата", null=True, blank=True)
    account = models.ForeignKey("root.Account", on_delete=models.CASCADE,
        related_name="revenue", verbose_name="Счёт")
    amount = models.IntegerField("Сумма")

    panels = [
        FieldRowPanel([
            *map(FieldPanel, ("sale", "date", "account", "amount")),
        ]),
    ]
