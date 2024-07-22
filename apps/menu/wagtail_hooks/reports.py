from django.urls import path, reverse

from wagtail import hooks
from wagtail.admin.menu import Menu, MenuItem, SubmenuMenuItem

from apps.reports.views import (
    ProductsReport, MoneyReport, ScrapReport, PriceListView,
    IncomeReport, AccountsReport
)


@hooks.register("register_admin_urls")
def register_reports_urls():
    return [
        path("products-report/", ProductsReport.as_view(), name="products_report"),
        path("income-report/", IncomeReport.as_view(), name="income_report"),
        path("accounts-report/", AccountsReport.as_view(), name="accounts_report"),
        path("money-report/", MoneyReport.as_view(), name="money_report"),
        path("scrap-report/", ScrapReport.as_view(), name="scrap_report"),
        path("prices-list/", PriceListView.as_view(), name="price_list"),
    ]


@hooks.register("register_admin_menu_item")
def register_reports_menu_item():
    submenu = Menu(items=[
        MenuItem("Товары", reverse("products_report"), icon_name="car-battery"),
        MenuItem("Доходы", reverse("income_report"), icon_name="money-check-dollar-pen"),
        MenuItem("Расчёты", reverse("accounts_report"), icon_name="money-calculator-24-filled"),
        MenuItem("Деньги", reverse("money_report"), icon_name="coins-fill"),
        MenuItem("Лом", reverse("scrap_report"), icon_name="car-battery"),
        MenuItem("Каталог", reverse("price_list"), icon_name="md-pricetags"),
    ])
    return SubmenuMenuItem("Отчёты", submenu, icon_name="histogram")
