import asyncio

from django.conf import settings

from contrib.utils.async_api_client import AsyncClient, async_api_client

AQSI_API_URL = "https://api.aqsi.ru/pub/v2"


class AQsi:
    def __init__(self):
        self.client = AsyncClient(
            AQSI_API_URL,
            default_headers={"x-client-key": f"Application {settings.AQSI_API_KEY}"}
        )

    async def shops_list(self):
        return await self.client.request("/Shops/list")

    async def goods_category_list(self):
        return await self.client.request("/GoodsCategory/list", log=True)

    async def goods_list(self):
        return await self.client.request("/Goods/list")

    async def bulk_upsert(self, data: bytes, endpoint: str):
        res = await self.client.request(endpoint, method="post", data={"file": data})
        _guid = res["guid"]
        _count = 10
        while True or _count > 0:
            await asyncio.sleep(1)
            res = await self.client.request(f"{endpoint}/{_guid}/status")
            if res["status"] != "inProgress":
                return res
            _count -= 1

    async def category_bulk_upsert(self, data: bytes):
        return await self.bulk_upsert(data, "/ListGoodsCategories")

    async def goods_bulk_upsert(self, data: bytes):
        return await self.bulk_upsert(data, "/ListGoods")


aqsi_client = async_api_client(AQsi)
