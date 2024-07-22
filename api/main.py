from ninja import NinjaAPI, Swagger

from contrib.ninja.auth import AuthBearer
from api.akbmag.routes import router as akbmag_router
from api.aqsi.routes import router as aqsi_router

app = NinjaAPI(
    title="Akb-Anapa API",
    auth=AuthBearer(),
    urls_namespace="api",
    docs=Swagger(settings=dict(persistAuthorization=True))
)

app.add_router("akbmag", akbmag_router, tags=["akbmag"])
app.add_router("aqsi", aqsi_router, tags=["aqsi"])
