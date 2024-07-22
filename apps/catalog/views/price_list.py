from django.http.response import FileResponse
from django.shortcuts import render

from ..excel import get_price_list_excel
from ..models import Product
from ..services import get_products, PriceListXmlPrepare


def price_list_view(request, renderer, extension, published=True):
    products = get_products(published=published)
    output = renderer(products)
    return FileResponse(output, as_attachment=True, filename=f"price_list.{extension}")


def catalog_view_excel(request):
    _file = get_price_list_excel()
    return FileResponse(_file, filename="catalog.xlsx")


def price_list_view_xml(request):
    products = get_products()
    _products = PriceListXmlPrepare(products).output
    return render(request, "root/price_list/price-list-template.xml", context={"products": _products})
