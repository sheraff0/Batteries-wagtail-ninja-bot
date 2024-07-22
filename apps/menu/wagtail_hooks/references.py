from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSetGroup

from apps.root.admin import FellowViewSet, PartnerViewSet, AccountViewSet, CountryViewSet
from apps.finance.admin import CostTypeViewSet
from apps.stock.admin import ScrapPriceViewSet


@register_snippet
class ReferencesGroup(SnippetViewSetGroup):
    menu_label = "Списки"
    menu_icon = "doc-full-inverse"
    items = (
        FellowViewSet, PartnerViewSet, AccountViewSet, CountryViewSet,
        CostTypeViewSet, ScrapPriceViewSet,
    )
