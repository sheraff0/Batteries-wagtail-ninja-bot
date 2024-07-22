from django.urls import path, reverse

from .views import products_report_excel, prices_excel


urlpatterns = [
    path("products-report/excel", products_report_excel, name="products_report_excel"),
    path("price-list/excel", prices_excel, name="prices_excel"),
]
