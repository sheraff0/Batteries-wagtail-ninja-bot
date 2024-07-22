import pandas as pd

from contrib.django.styling import intcomma

from ..sql.income import IncomeReport


def get_income_report(request, apply_intcomma=True):
    report = IncomeReport(request)
    _totals = report.execute()
    _totals = [
        {k: intcomma(v) if k != "ym" else v for k, v in x.items()}
        for x in _totals
    ]

    return {
        "totals": _totals
    }
