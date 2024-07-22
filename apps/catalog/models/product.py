import re

from django.conf import settings
from django.db import models
from django.db.models import Q, F, Value
from django.db.models.functions import Abs, Cast

from wagtail.models import PageQuerySet, PageManager
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel, FieldRowPanel
from wagtail.images import get_image_model

from apps.root.models.mixins import CommonPagesMixin, ImageMixin
from contrib.utils.html import unpack_elements
from contrib.wagtail.models import Page
from .common import (
    Polarity, PriceSegment, Terminal, CaseFormat, Sections, StandardSize,
    PREMIUM_GTE, DELTA_SIMILAR,
)
from .mixins import CatalogNavigationMixin


class ProductQuerySet(PageQuerySet):
    def published(self):
        return self.filter(published=True)

    def delta(self, fields, obj):
        qs = self
        for field in fields:
            _value = Cast(Value(getattr(obj, field)), output_field=models.FloatField())
            if _value is not None:
                qs = qs.annotate(**{
                    f"{field}__delta": Abs((_value - F(field)) / _value)
                })
        return qs

    def similar(self, fields, obj):
        return self.delta(fields, obj).filter(
            ~Q(pk=obj.pk),
            published=True,
        ).filter(
            Q(**{
                f"{field}__delta__lte": DELTA_SIMILAR
                for field in fields
            })
            | Q(standard_size=obj.standard_size)
        ).select_related("image").order_by("title")


class Product(CatalogNavigationMixin, ImageMixin, CommonPagesMixin, Page):
    # Sections
    section = models.PositiveSmallIntegerField("Секция", choices=Sections.choices,
        default=Sections.BATTERY, null=True, blank=True)
    published = models.BooleanField("Опубликовать на сайте", default=True)
    # Basic
    image = models.ForeignKey(get_image_model(), on_delete=models.SET_NULL,
        null=True, blank=True, verbose_name="Изображение")
    price = models.PositiveSmallIntegerField("Цена (полная)", null=True, blank=True)
    price_segment = models.PositiveSmallIntegerField("Ценовой сегмент", choices=PriceSegment.choices,
        null=True, blank=True)
    guarantee = models.PositiveSmallIntegerField("Гарантия, мес.", null=True, blank=True)
    description = RichTextField("Описание", null=True, blank=True)
    country = models.ForeignKey("root.Country", on_delete=models.SET_NULL, related_name="products",
        verbose_name="Страна", null=True, blank=True)
    # Battery specifications
    capacity = models.PositiveSmallIntegerField("Ёмкость, Ач", null=True, blank=True)
    current = models.PositiveSmallIntegerField("Пусковой ток, А", null=True, blank=True)
    polarity = models.PositiveSmallIntegerField("Полярность", choices=Polarity.choices,
        null=True, blank=True)
    terminal = models.PositiveSmallIntegerField("Клемма", choices=Terminal.choices,
        null=True, blank=True)
    # Battery dimensions
    length = models.PositiveSmallIntegerField("Длина, мм", null=True, blank=True)
    width = models.PositiveSmallIntegerField("Ширина, мм", null=True, blank=True)
    height = models.PositiveSmallIntegerField("Высота, мм", null=True, blank=True)
    low = models.BooleanField("Низкий", default=False)
    case_format = models.PositiveSmallIntegerField("Формат корпуса", choices=CaseFormat.choices,
        null=True, blank=True)
    standard_size = models.CharField("Типоразмер", max_length=16, choices=StandardSize.choices,
        null=True, blank=True)
    # Battery technologies
    calcium = models.BooleanField("Ca-Ca", default=False)
    efb = models.BooleanField("EFB", default=False)
    agm = models.BooleanField("AGM", default=False)
    silver = models.BooleanField("Silver", default=False)

    objects = PageManager.from_queryset(ProductQuerySet)()

    parent_page_types = ["Category"]
    subpage_types = []

    content_panels = Page.content_panels + [
        FieldRowPanel([*map(FieldPanel, ("section", "published"))]),
        FieldPanel("image"),
        FieldRowPanel([
            *map(FieldPanel, ("price", "price_segment", "guarantee")),
        ], heading="Преложение"),
        MultiFieldPanel([
            *map(FieldPanel, ("description", "country")),
        ], heading="Описание"),
        MultiFieldPanel([
            FieldRowPanel([*map(FieldPanel, ("capacity", "current"))]),
            FieldRowPanel([*map(FieldPanel, ("polarity", "terminal"))]),
        ], heading="Характеристики"),
        MultiFieldPanel([
            FieldRowPanel([*map(FieldPanel, ("standard_size", "length", "width", "height"))]),
            FieldRowPanel([*map(FieldPanel, ("case_format", "low",))]),
        ], heading="Размеры"),
        MultiFieldPanel([
            FieldRowPanel([*map(FieldPanel, ("calcium", "efb", "agm", "silver"))]),
        ], heading="Технологии"),
        InlinePanel("sales", label="Продажи", classname="collapsed"),
        InlinePanel("invoices", label="Поставки", classname="collapsed"),
    ]

    @property
    def discount(self):
        if self.section != Sections.BATTERY:
            return 0
        SCRAP_DISCOUNTS = (
            (220, 3000),
            (190, 2500),
            (140, 1800),
            (105, 1300),
            (100, 1200),
            (74, 1100),
            (60, 1000),
            (40, 600),
            (0, 0),
        )
        try:
            return next(discount
                for capacity, discount in SCRAP_DISCOUNTS
                if self.capacity >= capacity
            )
        except:
            return 0

    @property
    def price_discount(self):
        if self.price:
            return self.price - self.discount

    @property
    def premium(self):
        try:
            return self.price_segment >= PREMIUM_GTE
        except: ...

    @property
    def polarity_verbose(self):
        return dict(Polarity.choices).get(self.polarity)

    @property
    def case_format_verbose(self):
        return dict(CaseFormat.choices).get(self.case_format)

    @property
    def terminal_verbose(self):
        if self.terminal != Terminal.STANDARD:
            return dict(Terminal.choices).get(self.terminal)

    @property
    def low_verbose(self):
        return "низкий" if self.low else ""

    @property
    def dimensions(self):
        try:
            assert all((self.length, self.width, self.height))
            return " · ".join(map(str, (self.length, self.width, self.height)))
        except:
            return

    @property
    def technologies(self):
        _technologies = [
            ("calcium", "Ca/Ca"),
            ("efb", "EFB"),
            ("agm", "AGM"),
            ("silver", "Silver"),
        ]
        return ", ".join(v for k, v in _technologies
            if getattr(self, k, False))

    @property
    def specs(self):
        return [x for x in [
            ("Ёмкость", self.capacity, " Ач"),
            ("Пусковая сила тока", self.current, " А"),
            ("Полярность", self.polarity_verbose, ""),
            ("Клеммы", self.terminal_verbose, ""),
            ("Корпус", self.case_format_verbose, (self.standard_size or "") + (
                f" ({self.low_verbose})" if self.low_verbose else "")),
            ("Размеры", self.dimensions, "мм" if self.dimensions else ""),
            ("Страна производства", self.country and self.country.name, ""),
            ("Гарантия", self.guarantee, "мес."),
            ("Технологии", self.technologies, ""),
        ] if x[1] is not None]

    @property
    def similar(self):
        if self.section != Sections.BATTERY:
            return
        return self._meta.model.objects.similar([
            "capacity",
            "length", "width", "height",
            "case_format",
        ], self)

    def get_admin_display_title(self):
        return f"{self.title} - {self.price} ₽"

    @property
    def sku(self):
        return "{}-{:0>6}".format(self.section, self.id)

    @property
    def barcodes(self):
        return [re.sub(r"\D", "", self.sku)]

    @property
    def page_title(self):
        _res = self.title
        if self.section in (Sections.BATTERY, Sections.MOTO_BATTERY):
            _res = " ".join((self.get_section_display(), _res))
        return _res

    @property
    def description_text(self):
        try: return unpack_elements(self.description, join=" ")
        except: return self.description

    class Meta:
        verbose_name = "Товар"
