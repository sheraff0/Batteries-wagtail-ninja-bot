from wagtail.admin.viewsets.chooser import ChooserViewSet
from wagtail.snippets.views.snippets import SnippetViewSet

from .models import Invoice, ScrapPrice


class InvoiceViewSetBase:
    model = Invoice
    icon = "truck-fast"
    list_display = ("heading", "supply", "for_scrap", "paid", "debt", "payment_soon", "balance")
    search_fields = ("partner__name", "number")
    

class InvoiceViewSet(InvoiceViewSetBase, SnippetViewSet):
    def get_queryset(self, request):
        return self.model.objects.related().total_supply().total_paid().total_debt()


class InvoiceChooserViewSet(InvoiceViewSetBase, ChooserViewSet):
    form_fields = ("day", "partner", "number", "payment_date",
        "scrap_value", "scrap_weight")


class ScrapPriceViewSet(SnippetViewSet):
    model = ScrapPrice
    icon = "car-battery"
    list_display = ("__str__",)
