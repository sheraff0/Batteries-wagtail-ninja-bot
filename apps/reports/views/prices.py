from copy import deepcopy
from asgiref.sync import async_to_sync

from django.views.generic import TemplateView
from django.http.response import FileResponse

from apps.assets import catalog_data
from apps.catalog.services import CreateCatalog
from bridge.aqsi.services import bulk_upsert_catalog
from ..forms.prices import PriceListForm
from ..services.prices import get_prices_list
from ..excel import get_prices_excel


class PriceListView(TemplateView):
    template_name = "reports/prices-list.html"

    def post(self, request, *args, **kwargs):
        form = PriceListForm(request.POST, request.FILES)
        if form.is_valid():
            action = form.cleaned_data["action"]
            if action == "upload":
                _data = deepcopy(catalog_data)
                _data["products"] = form.cleaned_data["upload"]
                CreateCatalog(_data)()
            if action == "aqsi":
                async_to_sync(bulk_upsert_catalog)()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        _catalog = get_prices_list(self.request)
        return {
            **super().get_context_data(**kwargs),
            **_catalog,
        }


def prices_excel(request):
    _file = get_prices_excel(request)
    return FileResponse(_file, filename="prices.xlsx")
