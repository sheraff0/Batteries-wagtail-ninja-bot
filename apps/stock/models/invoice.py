from datetime import timedelta

from django.apps import apps
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q, F, Sum, OuterRef, Subquery
from django.db.models.functions import Cast
from django.utils.html import format_html

from modelcluster.models import ParentalKey, ClusterableModel

from wagtail.admin.panels import FieldPanel, FieldRowPanel, InlinePanel, HelpPanel
from wagtail.models import Orderable

from apps.root.models.common import DayMixin, ScrapMixin, BalanceMixin
from contrib.django.styling import style_text, color_text
from .mixins import DebtUrgencyMixin

PRICE_BIGINT = Cast("price", output_field=models.BigIntegerField())

class InvoiceQuerySet(models.QuerySet):
    def related(self):
        return self.select_related("day", "partner")

    def total_supply(self):
        InvoiceItem = apps.get_model("stock", "InvoiceItem")
        own_items = InvoiceItem.objects.values("invoice_id").filter(
            invoice_id=OuterRef("id")
        ).annotate(
            total=Sum(PRICE_BIGINT * F("quantity"))
        ).order_by("invoice_id")
        return self.annotate(
            total_supply=Subquery(own_items.values("total"))
        )

    @staticmethod
    def get_own_payments(in_debt=False):
        InvoicePayment = apps.get_model("finance", "InvoicePayment")
        _we_are_in_debt = Q(account__name__icontains="мы должны")
        return InvoicePayment.objects.values("invoice_id").filter(
            _we_are_in_debt if in_debt else ~_we_are_in_debt,
            invoice_id=OuterRef("id")
        ).annotate(
            total=Sum("amount")
        ).values("total").order_by("invoice_id")

    def total_paid(self):
        own_payments = self.get_own_payments(in_debt=False)
        return self.annotate(
            total_paid=Subquery(own_payments)
        )

    def total_debt(self):
        own_debts = self.get_own_payments(in_debt=True)
        return self.annotate(
            total_debt=Subquery(own_debts)
        )


class Invoice(
    DebtUrgencyMixin, BalanceMixin, DayMixin, ScrapMixin,
    ClusterableModel, Orderable
):
    day = ParentalKey("journal.Day", verbose_name="День",
        on_delete=models.PROTECT, related_name="invoices")
    partner = models.ForeignKey("root.Partner", verbose_name="Партнёр, поставщик",
        related_name="invoices", on_delete=models.PROTECT)
    number = models.CharField("Номер накладной", max_length=64, null=True, blank=True)
    date = models.DateField("Дата накладной", null=True, blank=True)
    payment_date = models.DateField("Срок оплаты", null=True, blank=True)

    comment = models.TextField("Комментарий", null=True, blank=True)

    panels = [
        FieldRowPanel([*map(FieldPanel, (
            "day", "partner", "number", "date"))]),
        FieldRowPanel([*map(FieldPanel, (
            "payment_date", "scrap_quantity", "scrap_value", "scrap_weight"))]),
        HelpPanel(template="stock/balance.html"),
        InlinePanel("items", label="Товары"),
        InlinePanel("payments", label="Платежи"),
        FieldPanel("comment"),
    ]

    objects = InvoiceQuerySet.as_manager()

    @property
    def heading(self):
        return f"№{self.number or '?'} от {self.date or '??.??.????'} ({self.partner.name})"

    @property
    def display_date(self):
        return self.date or self.day.date

    def _supply(self):
        return self.total_supply
    _supply.short_description = "Стоимость товаров"
    supply = property(_supply)

    def _for_scrap(self):
        return -self.scrap_value if self.scrap_value else None
    _for_scrap.short_description = "За лом"
    for_scrap = property(_for_scrap)

    def _paid(self):
        return self.total_paid
    _paid.short_description = "Оплачено"
    paid = property(_paid)

    @property
    def debit(self):
        try:
            _total_supply = self.total_supply
        except:
            _total_supply = self.items.model.objects.filter(invoice_id=self.id).aggregate(
                total=Sum(PRICE_BIGINT * F("quantity"))
            )["total"]
        return (_total_supply or 0) - (self.scrap_value or 0)

    @property
    def credit(self):
        try:
            _total_payments = (self.total_paid or 0) + (self.total_debt or 0)
        except:
            _total_payments = self.payments.model.objects.filter(invoice_id=self.id).aggregate(
                total=Sum("amount")
            )["total"]
        return _total_payments or 0

    def __str__(self):
        return self.heading

    class Meta:
        ordering = ["-day__date", "sort_order"]
        verbose_name = "Закупка"
        verbose_name_plural = "Закупки"


class InvoiceItem(Orderable):
    invoice = ParentalKey("stock.Invoice", verbose_name="Закупка",
        on_delete=models.CASCADE, related_name="items")
    product = ParentalKey("catalog.Product", verbose_name="Товар",
        on_delete=models.PROTECT, related_name="invoices")

    quantity = models.SmallIntegerField("Количество", default=1)
    price = models.PositiveSmallIntegerField("Цена закупки", default=0)

    panels = [
        *map(FieldPanel, ("invoice", "product")),
        FieldRowPanel([*map(FieldPanel, ("quantity", "price"))]),
    ]

    def __str__(self):
        return self.product.title if self.product else "-"

    class Meta:
        ordering = ["sort_order"]
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
