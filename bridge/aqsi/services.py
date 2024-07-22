from apps.catalog.services import CatalogTree, product_attrs
from external.aqsi.schemas import ListGoods, ListGoodsCategory
import external.aqsi.services as services


async def get_catalog_lists():
    def common_attrs_map(x):
        return dict(
            id=str(x["pk"]),
            number=x["order"],
            name=x["title"],
            parent=x.get("parent") and str(x["parent"]),
        )

    _tree = await CatalogTree()()
    return {
        "categories": ListGoodsCategory(payload=[common_attrs_map(x)
            for x in _tree["categories"]]),
        "products": ListGoods(payload=[dict(
            group_id=_common.pop("parent"),
            **_common,
            **{k: x[k] for k in product_attrs}
        ) for x in _tree["products"] if (_common := common_attrs_map(x))]),
    }


async def bulk_upsert_catalog():
    _data = await get_catalog_lists()
    _res_categories = await services.category_bulk_upsert(_data["categories"])
    _res_goods = await services.goods_bulk_upsert(_data["products"])
    return {
        "categories": _res_categories,
        "goods": _res_goods,
    }
