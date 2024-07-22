from django.db import models

from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.models import Page

from contrib.wagtail.panels import totals_controller_attrs


class Journal(Page):
    parent_page_types = ["root.Home"]
    subpage_types = ["Year"]

    max_count = 1

    class Meta:
        verbose_name = "Журнал"


class Year(Page):
    parent_page_types = ["Journal"]
    subpage_types = ["Month"]

    class Meta:
        verbose_name = "Год"


class Month(Page):
    parent_page_types = ["Year"]
    subpage_types = ["Day"]

    class Meta:
        verbose_name = "Месяц"


class Day(Page):
    date = models.DateField("Дата", unique=True)

    parent_page_types = ["Month"]
    subpage_types = []

    content_panels = Page.content_panels + [
        FieldPanel("date"),
        InlinePanel("work_shifts", label="Смены", classname="collapsed"),
        InlinePanel("sales", label="Продажи", classname="collapsed", **totals_controller_attrs),
        InlinePanel("invoices", label="Закупки", classname="collapsed", **totals_controller_attrs),
        InlinePanel("costs", label="Расходы", classname="collapsed"),
        InlinePanel("source_docs", label="Первичные документы", classname="collapsed"),
    ]

    def get_admin_display_title(self):
        return self.date

    class Meta:
        verbose_name = "День"
