from wagtail.admin.viewsets.chooser import ChooserViewSet
from wagtail.snippets.views.snippets import SnippetViewSet
from .models import Sale


class SaleViewSetBase:
    model = Sale
    icon = "barcode-reader"
    list_display = ("__str__", "date", "debit", "credit", "balance", "quantity", "price")
    search_fields = ("product__title",)


class SaleViewSet(SaleViewSetBase, SnippetViewSet):
    def get_queryset(self, request):
        return self.model.objects.related().total_payments()


class SaleChooserViewSet(SaleViewSetBase, ChooserViewSet):
    form_fields = ("day", "product", "quantity", "price",
        "scrap_value", "scrap_weight", "discount")
