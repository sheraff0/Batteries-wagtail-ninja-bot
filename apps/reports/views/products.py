from django.views.generic import TemplateView
from django.http.response import FileResponse

from ..services import get_products_report
from ..excel import get_products_report_excel


class ProductsReport(TemplateView):
    template_name = "reports/products-report.html"

    def get_context_data(self, **kwargs):
        _totals = get_products_report(self.request)
        return {
            **super().get_context_data(**kwargs),
            **_totals,
        }


def products_report_excel(request):
    _file = get_products_report_excel(request)
    return FileResponse(_file, filename="products.xlsx")
