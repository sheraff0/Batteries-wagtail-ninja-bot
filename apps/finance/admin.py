from wagtail.admin.viewsets.chooser import ChooserViewSet
from wagtail.snippets.views.snippets import SnippetViewSet

from .models import Cost, CostType


class CostTypeViewSetBase:
    model = CostType
    icon = "coins-fill"
    search_fields = ("name")


class CostTypeViewSet(CostTypeViewSetBase, SnippetViewSet):
    ...


class CostTypeChooserViewSet(CostTypeViewSetBase, ChooserViewSet):
    list_display = ("name", )
    form_fields = ("name", )


class CostViewSetBase:
    model = Cost
    icon = "coins-fill"
    search_fields = ("name",)
    list_display = ("__str__", "cost_type", "months", "debit", "credit", "balance")


class CostViewSet(CostViewSetBase, SnippetViewSet):
    def get_queryset(self, request):
        return self.model.objects.related().total_payments()


class CostChooserViewSet(CostViewSetBase, ChooserViewSet):
    form_fields = (
        "day", "cost_type", "name",
        "fellow", "partner", "amount",
        "comment",
    )
