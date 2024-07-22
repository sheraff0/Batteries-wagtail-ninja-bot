from django.urls import path
from .views import catalog_view_excel, price_list_view_xml

urlpatterns = [
    path("catalog/excel", catalog_view_excel, name="catalog_excel"),
    path("price-list/xml", price_list_view_xml, name="price_list_xml"),
]