from datetime import date

from django.db.models import Q

from contrib.common.filters import FilterSetBase, FiltersMixinBase
from contrib.utils.date_time import start_date, end_date


class DateFieldMixin:
    exclude_none = False

    def get_key(self, suffix):
        return "__".join(("__date", suffix))


class DateIntervalFilterSet(DateFieldMixin, FilterSetBase):
    filter_set = [
        ("start", str),
        ("end", str),
    ]

    def filter_start(self, value):
        return Q(**{self.get_key("gte"): start_date(value)})

    def filter_end(self, value):
        return Q(**{self.get_key("lte"): end_date(value)})


class BeforeStartFilterSet(DateFieldMixin, FilterSetBase):
    filter_set = [
        ("start", str),
    ]

    def filter_start(self, value):
        return Q(**{self.get_key("lt"): start_date(value)})
