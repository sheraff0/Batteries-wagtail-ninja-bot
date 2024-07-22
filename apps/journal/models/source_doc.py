import os
from uuid import uuid4

from django.db import models
from modelcluster.models import ParentalKey

from wagtail.admin.panels import FieldPanel, FieldRowPanel
from wagtail.models import Orderable

from apps.root.models.common import DayMixin


class SourceDocType(models.IntegerChoices):
    INVOICE = (1, "Накладная")
    JOURNAL = (2, "Журнал")


class SourceDoc(DayMixin, Orderable):
    def upload_to(self, filename):
        return os.path.join(
            "source_docs",
            *str(self.day.date).split("-"),
            str(uuid4()),
            filename
        )

    day = ParentalKey("journal.Day", verbose_name="День",
        on_delete=models.PROTECT, related_name="source_docs")
    source_doc_type = models.PositiveSmallIntegerField("Тип документа", choices=SourceDocType.choices,
        null=True, blank=True)
    name = models.CharField("Название", max_length=128, null=True, blank=True)

    document = models.FileField("Файл", upload_to=upload_to)

    panels = [
        FieldRowPanel([*map(FieldPanel, ("day", "source_doc_type", "document"))]),
        FieldPanel("name"),
    ]

    def delete(self, **kwargs):
        self.document.delete()
        return super().delete(**kwargs)

    class Meta:
        ordering = ["day__date", "sort_order"]
        verbose_name = "Первичный документ"
        verbose_name_plural = "Первичные документы"

    def _display_name(self):
        _source_doc_type_label = "???"
        try:
            _source_doc_type_label = SourceDocType(self.source_doc_type).label
        except: ...
        return f"{_source_doc_type_label} {self.name or self.document.file.name}"
    _display_name.short_description = "Название"
    display_name = property(_display_name)

    def __str__(self):
        return self.display_name
