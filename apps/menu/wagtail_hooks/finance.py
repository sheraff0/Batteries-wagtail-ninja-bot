from wagtail import hooks

from apps.finance.admin import CostTypeChooserViewSet


@hooks.register("register_admin_viewset")
def register_cost_type_chooser_viewset():
    return CostTypeChooserViewSet("cost_type")
