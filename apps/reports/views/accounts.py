from django.views.generic import TemplateView

from ..services import get_accounts_report


class AccountsReport(TemplateView):
    template_name = "reports/accounts-report.html"

    def get_context_data(self, **kwargs):
        _totals = get_accounts_report(self.request)
        return {
            **super().get_context_data(**kwargs),
            **_totals,
        }
