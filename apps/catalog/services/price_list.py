import bs4

from django.shortcuts import render

from wagtail.models import Page

from contrib.utils.excel.pandas import XlsxReader, XlsxWriter
from contrib.utils.patterns.pipeline import AbstractPipeline
from contrib.utils.html import unpack_elements
from ..models import Category, Product


def get_products(published=True):
    qs = Product.objects.live().select_related("image")
    if published:
        qs = qs.published()
    return qs


def get_categories_dict():
    return {x["path"]: x["title"] for x in Category.objects.values("path", "title")}


def get_catalog():
    _catalog = Catalog.objects.live().first()
    return Page.objects.filter(path__startswith=_catalog.path).values("path", "title", "content_type")


def get_path(product_path):
    _path = product_path
    _res = []
    _categories_dict = get_categories_dict()
    while len(_path) >= 20:
        _path = _path[:-4]
        _res.append(_categories_dict.get(_path))
    return "/".join(_res[::-1])


class PriceListStaticMethods:
    @staticmethod
    def efb_text(efb):
        return ("""
Аккумулятopныe батapeи серии ЕFB – это cпециaльнaя сeрия, в пеpвую очepeдь пpeдназначенная для aвтoмoбилей с сиcтeмой CTАPТ-СТОП."""
            if efb else "")

    @staticmethod
    def discount_text():
        return "Цeна указaнa c учётoм сдaчи cтapoгo aккумулятора такoй жe ёмкoсти."

    @staticmethod
    def delivery_text():
        return "Бесплатная доставка по городу."


class PriceListExcelPrepare(PriceListStaticMethods, AbstractPipeline):
    def process(self):
        return [{
            "section": x.section,
            "path": get_path(x.path),
            "title": x.title,
            "published": int(x.published) or "",
            "image": x.image and (
                str(x.image.file)
                .replace("original_images/products", "")
                .replace("original_images/", "")
            ) or "",
            "price": x.price,
            "price_segment": x.price_segment,
            "guarantee": x.guarantee,
            "description": x.description,
            "country": x.country and x.country.name or "",
            "capacity": x.capacity,
            "current": x.current,
            "standard_size": x.standard_size,
            "polarity": x.polarity,
            "terminal": x.terminal,
            "length": x.length,
            "width": x.width,
            "height": x.height,
            "low": int(x.low) or "",
            "case_format": x.case_format,
            "calcium": int(x.calcium) or "",
            "efb": int(x.efb) or "",
            "agm": int(x.agm) or "",
            "silver": int(x.silver) or "",
        } for x in self._source]


class PriceListXmlPrepare(PriceListStaticMethods, AbstractPipeline):
    def process(self):
        return [{
            "id": x.id,
            "name": x.title,
            "vendor": x.get_parent().title,
            "description": "\n".join((unpack_elements(x.description, join="\n"), self.efb_text(x.efb),
                self.discount_text(), self.delivery_text())),
            "short_description": unpack_elements(x.description)[0][:250],
            "price": x.price_discount,
            "picture": x.image and x.image.file.url,
            "url": x.full_url,
            "section": x.section,
        } for x in self._source]
