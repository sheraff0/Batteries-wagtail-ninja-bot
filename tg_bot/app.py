from fastapi import FastAPI, Depends, Request, Response
from fastapi.security import HTTPBearer

from telegram import Update
from telegram.ext import Application

from .security import secret_token


def get_app(bot_app: Application):
    app = FastAPI(docs_url=None, redoc_url=None)

    @app.post("/update", dependencies=[Depends(secret_token)])
    async def update_chat(request: Request) -> Response:
        await bot_app.update_queue.put(
            Update.de_json(data=await request.json(), bot=bot_app.bot)
        )
        return Response()

    return app
