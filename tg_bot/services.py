from apps.catalog.models import Product


async def get_products_count():
    return await Product.objects.all().acount()
