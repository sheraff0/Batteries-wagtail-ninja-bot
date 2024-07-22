from contrib.utils.gzip import GZipStream
from .api import aqsi_client, AQsi
from .schemas import ListGoodsCategory, ListGoods


@aqsi_client
async def shops_list(
    client: AQsi = None,
):
    return await client.shops_list()


@aqsi_client
async def goods_category_list(
    client: AQsi = None,
):
    return await client.goods_category_list()


@aqsi_client
async def goods_list(
    client: AQsi = None,
):
    return await client.goods_list()


@aqsi_client
async def bulk_upsert(
    data: ListGoodsCategory | ListGoods,
    resource: str,
    client: AQsi = None,
):
    _dump = data.model_dump_json()
    _file = GZipStream(_dump).output
    return await getattr(client, f"{resource}_bulk_upsert")(_file)


async def category_bulk_upsert(
    data: ListGoodsCategory,
):
    return await bulk_upsert(data, "category")


async def goods_bulk_upsert(
    data: ListGoods,
):
    return await bulk_upsert(data, "goods")
