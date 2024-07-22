from django.views.generic import TemplateView

from ..services import get_income_report


class IncomeReport(TemplateView):
    template_name = "reports/income-report.html"

    def get_context_data(self, **kwargs):
        _totals = get_income_report(self.request)
        return {
            **super().get_context_data(**kwargs),
            **_totals,
        }
