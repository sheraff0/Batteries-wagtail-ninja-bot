from django.db import models

from modelcluster.fields import ParentalKey

from wagtail.models import Orderable
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.images import get_image_model

from contrib.wagtail.models import Page
from .mixins import ImageMixin, CatalogSamplesMixin, CommonPagesMixin


class Home(CommonPagesMixin, CatalogSamplesMixin, Page):
    content_panels = Page.content_panels + [
        InlinePanel("slides", heading="Слайды"),
        InlinePanel("categories", heading="Категории"),
    ]

    subpage_types = ["catalog.Catalog", "Contacts", "journal.Journal"]

    @property
    def slides_list(self):
        return self.slides.select_related("image").all()

    @property
    def categories_list(self):
        return self.categories.select_related("image").all()


class HomeSlide(Orderable):
    page = ParentalKey("Home", on_delete=models.CASCADE, related_name="slides")
    image = models.ForeignKey(get_image_model(), on_delete=models.CASCADE, verbose_name="Изображение (PNG!)")

    subtitle = models.CharField("Над заголовком (проблема)", max_length=128, null=True, blank=True)
    title = models.CharField("Заголовок", max_length=128, null=True, blank=True)
    description = models.TextField("Описание", null=True, blank=True)
    details_title = models.CharField("Мотиватор", max_length=128, null=True, blank=True)
    details_subtitle = models.CharField("Мотиватор, дополнение", max_length=128, null=True, blank=True)

    class Meta:
        ordering = ["sort_order"]
        verbose_name = "Слайд"
        verbose_name_plural = "Слайды"


class HomeCategory(ImageMixin, Orderable):
    page = ParentalKey("Home", on_delete=models.CASCADE, related_name="categories")
    image = models.ForeignKey(get_image_model(), on_delete=models.CASCADE, verbose_name="Изображение (PNG!)")
    catalog_filters = models.CharField("Фильтры каталога", max_length=128, null=True, blank=True)

    title = models.CharField("Заголовок", max_length=128, null=True, blank=True)
    description = models.TextField("Описание", null=True, blank=True)

    class Meta:
        ordering = ["sort_order"]
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
