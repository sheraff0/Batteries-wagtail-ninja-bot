from django.conf import settings

from contrib.utils.excel.openpyxl import StreamToExcel, ExcelRendererBase
from ..services.price_list import get_products, PriceListExcelPrepare


ASSETS_DIR = settings.BASE_DIR / "apps/assets"


class PriceListRenderer(ExcelRendererBase):
    def process(self):
        _ws = self._template.active
        for i, item in enumerate(self._source, start=2):
            for j, value in enumerate(item.values(), start=1):
                _cell = _ws.cell(i, j, value)
        return self._template


def get_price_list_excel():
    _products = get_products(published=False)
    _template_path = ASSETS_DIR / "catalog_template.xlsx"
    return StreamToExcel(_products, _template_path, PriceListRenderer,
        before=[PriceListExcelPrepare]).output
