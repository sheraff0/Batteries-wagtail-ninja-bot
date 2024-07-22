from django.db.models import Q, F, Sum, OuterRef, Subquery
from django.db.models.functions import Coalesce

from contrib.django.styling import intcomma

from apps.finance.models import CostPayment, SalePayment, InvoicePayment
from apps.root.models import Account
from contrib.django.querysets import get_totals_by_id
from ..filters import DateIntervalFilterSet, BeforeStartFilterSet


def get_accounts_totals_queryset(request):
    # Filters
    _before_filter = BeforeStartFilterSet(request).filters
    _interval_filter = DateIntervalFilterSet(request).filters
    # Date fields
    _sale_payment_date_field = Coalesce(F("date"), F("sale__day__date"))
    _invoice_payment_date_field = Coalesce(F("date"), F("invoice__day__date"))
    _cost_payment_date_field = Coalesce(F("date"), F("cost__day__date"))
    # Subqueries
    _own_income_before = get_totals_by_id(
        SalePayment, "account", "amount", _sale_payment_date_field, _before_filter)
    _own_expense_before = get_totals_by_id(
        InvoicePayment, "account", "amount", _invoice_payment_date_field, _before_filter)
    _own_cost_before = get_totals_by_id(
        CostPayment, "account", "amount", _cost_payment_date_field, _before_filter)
    _own_income = get_totals_by_id(
        SalePayment, "account", "amount", _sale_payment_date_field, _interval_filter)
    _own_expense = get_totals_by_id(
        InvoicePayment, "account", "amount", _invoice_payment_date_field, _interval_filter)
    _own_cost = get_totals_by_id(
        CostPayment, "account", "amount", _cost_payment_date_field, _interval_filter)
    return Account.objects.annotate(
        income_before=Subquery(_own_income_before),
        expense_before=Subquery(_own_expense_before),
        cost_before=Subquery(_own_cost_before),
        balance_start=Coalesce(F("income_before"), 0) \
            - Coalesce(F("expense_before"), 0) - Coalesce(F("cost_before"), 0),
        _income=Subquery(_own_income),
        income=Coalesce(F("_income"), 0),
        _expense=Subquery(_own_expense),
        _cost=Subquery(_own_cost),
        expense=-Coalesce(F("_expense"), 0) - Coalesce(F("_cost"), 0),
    )


def get_money_report(request):
    _calculated = ["balance_start", "income", "expense"]
    _totals = get_accounts_totals_queryset(request).values("id", "name", *_calculated)
    _totals = [{**x,
        "balance_end": x["balance_start"] + x["income"] + x["expense"]
    } for x in _totals]
    _calculated.append("balance_end")
    _totals.insert(0, {"id": 0, "name": "Всего", **{
        key: sum(x[key] for x in _totals) for key in _calculated}})
    _totals = [{**x,
        **{attr: intcomma(x[attr]) for attr in _calculated},
    } for x in _totals]
    return _totals
