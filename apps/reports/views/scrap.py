from django.views.generic import TemplateView
from django.http.response import FileResponse

from ..services import get_scrap_report


class ScrapReport(TemplateView):
    template_name = "reports/scrap-report.html"

    def get_context_data(self, **kwargs):
        _totals = get_scrap_report(self.request)
        return {
            **super().get_context_data(**kwargs),
            **_totals,
        }
