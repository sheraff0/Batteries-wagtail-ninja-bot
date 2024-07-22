from wagtail.admin.viewsets.chooser import ChooserViewSet
from wagtail.snippets.views.snippets import SnippetViewSet

from .models import Country, Fellow, Partner, Account


class FellowViewSetBase:
    model = Fellow
    icon = "group"
    search_fields = ("name",)


class FellowViewSet(FellowViewSetBase, SnippetViewSet):
    list_display = ("name",)


class FellowChooserViewSet(FellowViewSetBase, ChooserViewSet):
    form_fields = ("name",)


class PartnerViewSetBase:
    model = Partner
    icon = "handshake-o"
    search_fields = ("name",)


class PartnerViewSet(PartnerViewSetBase, SnippetViewSet):
    list_display = ("name",)


class PartnerChooserViewSet(PartnerViewSetBase, ChooserViewSet):
    form_fields = ("name",)


class AccountViewSetBase:
    model = Account
    icon = "money-check-dollar-pen"
    search_fields = ("name",)


class AccountViewSet(AccountViewSetBase, SnippetViewSet):
    list_display = ("name",)


class AccountChooserViewSet(AccountViewSetBase, ChooserViewSet):
    form_fields = ("name",)


class CountryViewSetBase:
    model = Country
    icon = "site"
    search_fields = ("name",)


class CountryViewSet(CountryViewSetBase, SnippetViewSet):
    list_display = ("name",)


class CountryChooserViewSet(CountryViewSetBase, ChooserViewSet):
    form_fields = ("name",)
