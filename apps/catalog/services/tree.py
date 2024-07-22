from django.apps import apps

common_attrs = ("pk", "path", "title")
product_attrs = ("price", "sku", "barcodes")


class CatalogTree:
    async def set_categories_index(self):
        Category = apps.get_model("catalog", "Category")
        self._categories_index = {x["path"]: x async for x in
            Category.objects.values(*common_attrs).order_by("path")}

    def with_tree_attrs(self, qs):
        return [{**x,
                "parent": _parent and _parent["pk"],
                "order": i,
            } for i, x in enumerate(qs, start=1)
            if (_parent := self._categories_index.get(x.pop("path")[:-4])) or True
        ]

    async def set_categories(self):
        await self.set_categories_index()
        self._categories = self.with_tree_attrs(self._categories_index.values())
    
    async def set_products(self):
        Product = apps.get_model("catalog", "Product")
        qs = [{
            k: getattr(x, k, None)
            for k in (*common_attrs, *product_attrs)
        } async for x in Product.objects.all()]
        self._products = self.with_tree_attrs(qs)

    async def set(self):
        await self.set_categories()
        await self.set_products()

    @property
    def categories(self):
        return self._categories

    @property
    def products(self):
        return self._products

    async def __call__(self):
        await self.set()
        return {
            "categories": self.categories,
            "products": self.products,
        }
