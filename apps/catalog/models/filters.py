from django.db.models import Q

from contrib.common.filters import FilterSetBase, FiltersMixinBase
from apps.root.models.common import PREMIUM_GTE


class CatalogFilterSet(FilterSetBase):
    filter_set = [
        ("section", int),
        ("premium", bool),
        ("case_format", int),
        ("capacity__gte", int),
        ("capacity__lte", int),
        ("current__gte", int),
        ("current__lte", int),
        ("length__gte", int),
        ("length__lte", int),
        ("width__gte", int),
        ("width__lte", int),
        ("height__gte", int),
        ("height__lte", int),
        ("polarity", int)
    ]

    def filter_premium(self, value):
        return Q(price_segment__gte=PREMIUM_GTE)


class CatalogFiltersMixin(FiltersMixinBase):
    filter_set_class = CatalogFilterSet
