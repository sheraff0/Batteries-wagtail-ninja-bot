from django.db import models
from modelcluster.fields import ParentalKey

from wagtail.admin.panels import FieldPanel, FieldRowPanel
from wagtail.models import Orderable


class InvoicePayment(Orderable):
    invoice = ParentalKey("stock.Invoice", on_delete=models.CASCADE,
        related_name="payments", verbose_name="Закупка")
    date = models.DateField("Дата", null=True, blank=True)
    account = models.ForeignKey("root.Account", on_delete=models.CASCADE,
        related_name="supply", verbose_name="Счёт")
    amount = models.IntegerField("Сумма")

    panels = [
        FieldRowPanel([
            *map(FieldPanel, ("invoice", "date", "account", "amount")),
        ]),
    ]
