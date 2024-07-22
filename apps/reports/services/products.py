from contrib.django.styling import intcomma
from contrib.wagtail.pages import get_page_edit_url
from ..sql.products import ProductsReport, CALCULATED


def get_products_report(request, apply_intcomma=True):
    report = ProductsReport(request)
    _totals = report.execute()
    _totals = [{**x,
        "edit_url": get_page_edit_url(x["id"]),
    } for x in _totals]
    if apply_intcomma:
        _totals = [{**x,
            **{attr: intcomma(x[attr]) for attr in CALCULATED + [
                "margin", "margin_percent", "margin_with_scrap", "amount_end"]}
        } for x in _totals]
    return {
        "request": request,
        "totals": _totals
    }
