from django.apps import apps
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Sum, OuterRef, Subquery

from modelcluster.models import ParentalKey, ClusterableModel

from wagtail.admin.panels import FieldRowPanel, FieldPanel, InlinePanel, HelpPanel
from wagtail.models import Orderable

from apps.root.models.common import SimpleModel, BalanceMixin


class CostQuerySet(models.QuerySet):
    def related(self):
        return self.select_related("day", "cost_type", "fellow", "partner")

    def total_payments(self):
        CostPayment = apps.get_model("finance", "CostPayment")
        own_payments = CostPayment.objects.values("cost_id").filter(
            cost_id=OuterRef("id")
        ).annotate(
            total=Sum("amount")
        ).values("total")
        return self.annotate(
            total_payments=Subquery(own_payments)
        )


class CostType(SimpleModel, ClusterableModel):
    ...

    class Meta:
        verbose_name = "Тип расходов"
        verbose_name_plural = "Типы расходов"


class Cost(BalanceMixin, SimpleModel, Orderable, ClusterableModel):
    day = ParentalKey("journal.Day", verbose_name="День", on_delete=models.PROTECT, related_name="costs")
    cost_type = ParentalKey(CostType, verbose_name="Тип расходов",
        on_delete=models.SET_NULL, null=True, blank=True, related_name="costs")

    fellow = models.ForeignKey("root.Fellow", verbose_name="Сотрудник",
        on_delete=models.SET_NULL, null=True, blank=True, related_name="fees")
    partner = models.ForeignKey("root.Partner", verbose_name="Партнёр, поставщик",
        related_name="costs", on_delete=models.SET_NULL, null=True, blank=True)

    amount = models.IntegerField("Сумма")
    months = models.IntegerField("На сколько месяцев?", default=1, validators=[MinValueValidator(1)])

    comment = models.TextField("Комментарий", null=True, blank=True)

    panels = [
        FieldRowPanel([
            *map(FieldPanel, ("day", "cost_type", "name")),
        ]),
        HelpPanel(template="stock/balance.html"),
        FieldRowPanel([
            *map(FieldPanel, ("fellow", "partner", "amount", "months")),
        ]),
        FieldPanel("comment"),
        InlinePanel("payments", label="Платежи"),
    ]

    objects = CostQuerySet.as_manager()

    def _debit(self):
        return self.amount
    _debit.short_description = "Затрачено"
    debit = property(_debit)

    def _credit(self):
        try:
            _total_payments = self.total_payments
        except:
            _total_payments = self.payments.model.objects.filter(cost_id=self.id).aggregate(
                total=Sum("amount")
            )["total"]
        return _total_payments or 0
    _credit.short_description = "Оплачено"
    credit = property(_credit)

    def __str__(self):
        return f"{self.day.date} - {self.name} - {self.amount}"

    class Meta:
        verbose_name = "Расход"
        verbose_name_plural = "Расходы"


class CostPayment(Orderable):
    cost = ParentalKey(Cost, on_delete=models.CASCADE,
        related_name="payments", verbose_name="Расход")
    date = models.DateField("Дата", null=True, blank=True)
    account = models.ForeignKey("root.Account", on_delete=models.CASCADE,
        related_name="costs", verbose_name="Счёт")
    amount = models.IntegerField("Сумма")

    panels = [
        FieldRowPanel([
            *map(FieldPanel, ("cost", "date", "account", "amount")),
        ]),
    ]
