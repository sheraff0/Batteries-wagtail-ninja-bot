from django.conf import settings

from ninja import Router

from external.akbmag.scrape import akbmag_scraper, search_akb

router = Router()


async def get_root(request):
    r = akbmag_scraper.parse_root()
if settings.DEBUG:
    router.get("/root")(get_root)


@router.get("/search", auth=None)
async def search(request,
    q: str | None = None,
):
    return await search_akb(q)
