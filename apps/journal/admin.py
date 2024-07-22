from wagtail.snippets.views.snippets import SnippetViewSet
from .models import SourceDoc


class SourceDocViewSet(SnippetViewSet):
    model = SourceDoc
    icon = "invoice-solid"
    list_display = ("display_name", "date")
