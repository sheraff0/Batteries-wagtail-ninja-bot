from django.db import models

from contrib.django.styling import mark_validated

PREMIUM_GTE = 5


class SimpleModel(models.Model):
    name = models.CharField("Название", max_length=64)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class DayMixin:
    @property
    def date(self):
        return self.day.date


class ScrapMixin(models.Model):
    scrap_quantity = models.SmallIntegerField("Лом, штуки", default=0)
    scrap_weight = models.SmallIntegerField("Прием лома, кг", default=0)
    scrap_value = models.IntegerField("Оценка лома", default=0)

    class Meta:
        abstract = True


class BalanceMixin:
    @mark_validated([lambda x: x == 0])
    def _balance(self):
        return self.debit - self.credit
    _balance.short_description = "Баланс"
    balance = property(_balance)

