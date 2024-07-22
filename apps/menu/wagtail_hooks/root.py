from wagtail import hooks

from apps.root.admin import (
    FellowChooserViewSet,
    PartnerChooserViewSet,
    AccountChooserViewSet,
    CountryChooserViewSet,
)


@hooks.register("register_admin_viewset")
def register_fellow_chooser_vewset():
    return FellowChooserViewSet("fellows")


@hooks.register("register_admin_viewset")
def register_partner_chooser_vewset():
    return PartnerChooserViewSet("partners")


@hooks.register("register_admin_viewset")
def register_account_chooser_vewset():
    return AccountChooserViewSet("payment-accounts")


@hooks.register("register_admin_viewset")
def register_country_chooser_vewset():
    return CountryChooserViewSet("countries")
