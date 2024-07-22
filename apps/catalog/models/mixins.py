from django.apps import apps
from django.db.models import OuterRef, Exists
from django.db.models.functions import Length

from wagtail.models import Page

from apps.root.models.mixins import ProductsMixin
from .filters import CatalogFiltersMixin


class CatalogProductsMixin(CatalogFiltersMixin, ProductsMixin):
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        _filters = self.get_filters(request)
        return {
            **context,
            "products": self.get_products(filters=_filters),
        }


class CatalogNavigationMixin:
    def get_breadcrumbs(self):
        _path = self.path
        _len = len(_path)
        return Page.objects.filter(
            path__in=[_path[:x] for x in range(8, _len, 4)]
        )

    def get_related_pages_base(self):
        Product = apps.get_model("catalog", "Product")
        own_products = Product.objects.filter(
            path__startswith=OuterRef("path"),
            published=True,
        )
        return Page.objects.annotate(
            length=Length("path"),
        ).annotate(
            has_products=Exists(own_products)
        ).filter(
            has_products=True,
            content_type__model="category",
        )

    def get_children_pages(self):
        _qs = self.get_related_pages_base()
        return _qs.filter(
            path__startswith=self.path,
            length=len(self.path) + 4,
        )

    def get_siblings(self):
        _qs = self.get_related_pages_base()
        return _qs.filter(
            path__startswith=self.path[:-4],
            length=len(self.path),
        )

    def get_search_for(self, request):
        return request.GET.get("search_for")

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        return {
            **context,
            "breadcrumbs": self.get_breadcrumbs(),
            "children": self.get_children_pages(),
            "siblings": self.get_siblings(),
            "search_for": self.get_search_for(request),
        }
