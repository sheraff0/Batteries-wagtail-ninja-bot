from django.db import models
    
from wagtail.admin.panels import FieldPanel


class Fellow(models.Model):
    name = models.CharField("Имя", max_length=64)
    birth_day = models.DateField("День рождения", null=True, blank=True)

    panels = [
        FieldPanel("name"),
    ]

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"
