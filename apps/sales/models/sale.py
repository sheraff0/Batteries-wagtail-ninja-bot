from django.apps import apps
from django.db import models
from django.db.models import Sum, OuterRef, Subquery

from modelcluster.models import ParentalKey, ClusterableModel

from wagtail.admin.panels import FieldPanel, FieldRowPanel, InlinePanel, HelpPanel
from wagtail.models import Orderable
from wagtail.fields import StreamField

from apps.root.models.common import DayMixin, ScrapMixin, BalanceMixin


class SaleQuerySet(models.QuerySet):
    def related(self):
        return self.select_related("day", "product")

    def total_payments(self):
        SalePayment = apps.get_model("finance", "SalePayment")
        own_payments = SalePayment.objects.values("sale_id").filter(
            sale_id=OuterRef("id")
        ).annotate(
            total=Sum("amount")
        ).values("total").order_by("sale_id")
        return self.annotate(
            total_payments=Subquery(own_payments)
        )


class Sale(BalanceMixin, DayMixin, ScrapMixin, Orderable, ClusterableModel):
    day = ParentalKey("journal.Day", verbose_name="День",
        on_delete=models.PROTECT, related_name="sales")
    product = ParentalKey("catalog.Product", verbose_name="Товар",
        on_delete=models.SET_NULL, null=True, blank=True, related_name="sales")

    quantity = models.SmallIntegerField("Количество", default=1)
    price = models.PositiveIntegerField("Цена полная (за 1 ед.)", default=0)
    discount = models.PositiveIntegerField("Комиссии, скидки", default=0)

    fellow = models.ForeignKey("root.Fellow", verbose_name="Сотрудник",
        on_delete=models.SET_NULL, null=True, blank=True, related_name="sales")

    comment = models.TextField("Комментарий", null=True, blank=True)

    panels = [
        FieldRowPanel([*map(FieldPanel, ("day", "product", "fellow"))]),
        HelpPanel(template="stock/balance.html"),
        FieldRowPanel([*map(FieldPanel, (
            "quantity", "price", "discount"))]),
        FieldRowPanel([*map(FieldPanel, (
            "scrap_quantity", "scrap_value", "scrap_weight"))]),
        InlinePanel("payments", label="Платежи", min_num=1),
        FieldPanel("comment"),
    ]

    objects = SaleQuerySet.as_manager()

    def _debit(self):
        try:
            return self.total_payments or 0
        except:
            return self.payments.model.objects.filter(sale_id=self.id).aggregate(
                total=Sum("amount")
            )["total"] or 0

    _debit.short_description = "Получено"
    debit = property(_debit)

    def _credit(self):
        return (
            self.quantity * self.price
        ) - (
            self.scrap_value or 0
        ) - (
            self.discount or 0
        )
    _credit.short_description = "Продано"
    credit = property(_credit)

    def __str__(self):
        return self.product and self.product.title or self.comment or "-"

    class Meta:
        ordering = ["-day__date", "sort_order"]
        verbose_name = "Продажа"
        verbose_name_plural = "Продажи"
