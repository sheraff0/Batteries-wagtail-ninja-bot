from django.views.generic import TemplateView

from ..services import get_money_report


class MoneyReport(TemplateView):
    template_name = "reports/money-report.html"

    def get_context_data(self, **kwargs):
        _totals = get_money_report(self.request)
        return {
            **super().get_context_data(**kwargs),
            "totals": _totals
        }
