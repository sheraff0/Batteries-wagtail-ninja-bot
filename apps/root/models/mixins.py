import random

from django.apps import apps
from django.conf import settings
from django.templatetags.static import static
from django.db.models import Q

from wagtail.models import Page

from .common import PREMIUM_GTE


class ImageMixin:
    @property
    def image_url(self):
        try:
            return self.image.file.url
        except:
            return static("img/placeholder.png")


class CommonPagesMixin:
    def get_common_pages(self):
        models = ["root.Home", "root.Contacts", "catalog.Catalog"]
        return {
            _model.lower(): _obj
            for _app, _model in (x.split(".") for x in models)
            if (_Model := apps.get_model(_app, _model))
            (_obj := _Model.objects.live().first())
        }

    def get_context(self, request):
        _common_pages = self.get_common_pages()
        return {
            **super().get_context(request),
            "common_pages": _common_pages,
            "DEBUG": settings.DEBUG,
            "YANDEX_METRIKA": settings.YANDEX_METRIKA,
        }


class ProductsMixin:
    def get_products(self, filters=list(), ids=False, shuffle=False):
        Product = apps.get_model("catalog", "Product")
        qs = Product.objects.live().published().filter(
            *filters,
            price__gt=0,
            path__startswith=self.path,
        ).select_related("image", "country").order_by("path")
        if ids:
            qs = qs.values_list("pk", flat=True)
        qs = list(qs)
        if shuffle:
            random.shuffle(qs)
        return qs

    def get_optimum(self, n=6):
        _ids = self.get_products(filters=[Q(
            price_segment__lt=PREMIUM_GTE
        )], ids=True)
        _ids = random.sample(_ids, n)
        return self.get_products(filters=[Q(id__in=_ids)], shuffle=True)

    def get_premium(self):
        return self.get_products(filters=[Q(price_segment__gte=PREMIUM_GTE)])


class CatalogSamplesMixin(ProductsMixin):
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        return {
            **context,
            "optimum": self.get_optimum(),
            "premium": self.get_premium(),
        }
