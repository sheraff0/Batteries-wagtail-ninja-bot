from dataclasses import dataclass
from datetime import date

from apps.stock.models.mixins import DebtUrgencyMixin
from contrib.django.styling import intcomma, color_text
from contrib.wagtail.pages import get_page_edit_url

from ..sql.accounts import AccountsReport


@dataclass
class DebtUrgency(DebtUrgencyMixin):
    total_debt: int
    payment_date: date


def get_accounts_report(request, apply_intcomma=True):
    report = AccountsReport(request)
    _totals = report.execute()
    _totals = [{**x,
        "edit_url": get_page_edit_url(x["id"], path="snippets/stock/invoice/edit/{id}/"),
    } for x in _totals]
    if apply_intcomma:
        _totals = [{**x,
            **{attr: intcomma(x[attr]) for attr in ("supply", "paid", "scrap", "advance")}
        } for x in _totals]

        _totals_styled = []
        for x in _totals:
            _debt, _payment_date = map(x.get, ("debt", "payment_date"))
            if _payment_date:
                _styled = DebtUrgency(_debt, _payment_date)
                x["debt"] = intcomma(_styled.debt)
                x["payment_date"] = _styled.payment_soon
            else:
                x["debt"] = intcomma(_debt)
            _totals_styled.append(x)

    return {
        "totals": _totals
    }
