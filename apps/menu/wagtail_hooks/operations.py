from wagtail import hooks
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSetGroup

from apps.journal.admin import SourceDocViewSet
from apps.sales.admin import SaleViewSet, SaleChooserViewSet
from apps.stock.admin import InvoiceViewSet, InvoiceChooserViewSet
from apps.finance.admin import CostViewSet, CostChooserViewSet


@register_snippet
class OperationsGroup(SnippetViewSetGroup):
    menu_label = "Операции"
    menu_icon = "edit"
    items = [SaleViewSet, InvoiceViewSet, CostViewSet, SourceDocViewSet]


@hooks.register("register_admin_viewset")
def register_sale_chooser_viewset():
    return SaleChooserViewSet("sales")


@hooks.register("register_admin_viewset")
def register_invoice_chooser_viewset():
    return InvoiceChooserViewSet("invoices")


@hooks.register("register_admin_viewset")
def register_cost_chooser_viewset():
    return CostChooserViewSet("costs")
