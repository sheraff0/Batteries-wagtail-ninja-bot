import numpy as np

from django.db.models import Q, F, Sum
from django.db.models.functions import Length, Coalesce

from contrib.django.styling import intcomma
from contrib.wagtail.pages import get_page_edit_url
from apps.catalog.models import Sections
from apps.catalog.services import get_catalog
from apps.sales.models import Sale
from apps.stock.models import Invoice
from contrib.django.querysets import SumProduct, get_totals
from contrib.utils.numpy import array_from_dict
from ..filters import DateIntervalFilterSet, BeforeStartFilterSet

common_scrape_fields = ("scrap_quantity", "scrap_weight", -F("scrap_value"))
restored_sold_fields = ("quantity", 0, SumProduct)


def get_scrap_totals_tuple(Model, targets=common_scrape_fields, date_field=F("day__date"), filters=list()):
    _targets_tuples = [(f"target_{i}", x) for i, x in enumerate(targets)]
    print(_targets_tuples)
    return tuple(x or 0 for x in get_totals(Model, _targets_tuples,
        date_field=date_field, filters=filters).values())


def get_scrap_totals_matrix(request, Model, targets=common_scrape_fields, date_field=F("day__date"), filters=list()):
    _before_filters = BeforeStartFilterSet(request).filters
    _interval_filters = DateIntervalFilterSet(request).filters
    _mapper = lambda x: np.array(
        get_scrap_totals_tuple(Model, targets=targets, date_field=date_field, filters=[*x, *filters]))
    _before, _interval = map(_mapper, (_before_filters, _interval_filters))
    return np.stack([_before, _interval, _before + _interval])


def get_recovered_filter(restored_field):
    return Q(**{F"{restored_field}__icontains": "восстановлен"})


def get_scrap_totals(request):
    # Date fields
    _invoice_date_field = Coalesce(F("payment_date"), F("day__date"))
    # Filters
    _recovered_filter_sale = get_recovered_filter("product__title")
    _recovered_filter_invoice = get_recovered_filter("partner__name")
    # Queries
    _accepted = get_scrap_totals_matrix(request, Sale)
    _disposed = - get_scrap_totals_matrix(request, Invoice,
        date_field=_invoice_date_field, filters=[~_recovered_filter_invoice])
    _restored = - get_scrap_totals_matrix(request, Invoice, filters=[_recovered_filter_invoice])
    _restored_sold = get_scrap_totals_matrix(request, Sale, targets=restored_sold_fields,
        filters=[_recovered_filter_sale])
    _restored_sold_clean = np.copy(_restored_sold)
    _restored_sold_clean[:,0] = 0
    _total = _accepted + _disposed + _restored + _restored_sold_clean
    return {
        "accepted": _accepted,
        "disposed": _disposed,
        "restored": _restored,
        "restored_sold": _restored_sold,
        "total": _total,
    }


def get_scrap_report(request, apply_intcomma=True):
    _totals = get_scrap_totals(request)
    _totals = {k: [*map(np.vectorize(intcomma), v)] for k, v in _totals.items()}
    return {
        "request": request,
        "totals": _totals
    }
