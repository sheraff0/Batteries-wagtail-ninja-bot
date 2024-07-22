import asyncio

import uvicorn

from django.conf import settings

from telegram import Update

from config.wsgi import application
from .app import get_app
from .bot import AkbAnapaBot


async def main_webhook(bot: AkbAnapaBot) -> None:
    await bot.set_menu_button()
    await bot.set_webhook()
    app = get_app(bot.app)

    webserver = uvicorn.Server(
        uvicorn.Config(
            app=app,
            host="0.0.0.0",
            port=8000,
        )
    )

    async with bot.app:
        await bot.app.start()
        await webserver.serve()
        await bot.app.stop()


if __name__ == "__main__":
    bot = AkbAnapaBot()
    loop = asyncio.get_event_loop()

    if settings.DEBUG:
        loop.run_until_complete(bot.set_menu_button())
        bot.app.run_polling()
    else:
        loop.run_until_complete(main_webhook(bot))
