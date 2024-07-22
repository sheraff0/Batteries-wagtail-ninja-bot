from contrib.django.styling import intcomma
from contrib.wagtail.pages import get_page_edit_url

from ..sql.prices import PriceList


def get_prices_list(request, apply_intcomma=True):
    report = PriceList(request)
    _catalog = report.execute()
    _catalog = [{**x,
        "edit_url": get_page_edit_url(x["id"]),
    } for x in _catalog]
    if apply_intcomma:
        _catalog = [{**x,
            **{attr: intcomma(x[attr]) for attr in [
                "price", "quantity", "sold"]}
        } for x in _catalog]
    return {
        "catalog": _catalog
    }
