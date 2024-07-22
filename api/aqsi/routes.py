from django.http import FileResponse, HttpResponse

from ninja import Router, File

import bridge.aqsi.services as services

router = Router()


@router.get("/shops-list")
async def shops_list(request):
    return await services.shops_list()


@router.get("/goods-category-list")
async def goods_category_list(request):
    return await services.goods_category_list()


@router.get("/goods-list")
async def goods_list(request):
    return await services.goods_list()


@router.get("/bulk-upsert-catalog")
async def bulk_upsert_catalog(request):
    return await services.bulk_upsert_catalog()
