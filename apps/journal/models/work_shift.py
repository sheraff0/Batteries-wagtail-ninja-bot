from django.db import models

from modelcluster.models import ParentalKey

from wagtail.admin.panels import FieldPanel, FieldRowPanel
from wagtail.models import Orderable


class WorkShift(models.Model):
    day = ParentalKey("journal.Day", verbose_name="День", on_delete=models.CASCADE,
        related_name="work_shifts")
    fellow = models.ForeignKey("root.Fellow", verbose_name="Сотрудник",
        on_delete=models.SET_NULL, null=True, blank=True, related_name="work_shifts")
    start_time = models.TimeField("Начало смены")
    end_time = models.TimeField("Окончание смены")

    panels = [
        FieldRowPanel([*map(FieldPanel, (
            "day", "fellow", "start_time", "end_time"
        ))])
    ]

    class Meta:
        verbose_name = "Рабочая смена"
        verbose_name_plural = "Рабочая смена"
