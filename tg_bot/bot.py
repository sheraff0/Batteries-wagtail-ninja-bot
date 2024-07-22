import orjson
from urllib.parse import urlencode
from uuid import uuid4

from django.conf import settings

from telegram import (
    ForceReply, Update,
    InlineKeyboardMarkup, InlineKeyboardButton,
)
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CommandHandler, MessageHandler,
    ConversationHandler,
    CallbackQueryHandler,
    ContextTypes, filters,
)

from contrib.common.redis import redis_client
from external.akbmag.scrape import search_akb, get_url_params

API_URL = "https://tg.акб-анапа.рф"
SEARCH = 1


class AkbAnapaBot:
    def __init__(self, cache_ttl: int = 900):
        self._app = Application.builder().token(
            settings.TELEGRAM_BOT_ACCESS_TOKEN).build()

        pickup_handler = ConversationHandler(
            entry_points=[CommandHandler("pickup", self.pick_up)],
            states={
                SEARCH: [
                    MessageHandler(filters.TEXT, self.search),
                    CallbackQueryHandler(self.callback),
                ]
            },
            fallbacks=[CommandHandler("cancel", self.cancel)],
        )

        self._app.add_handler(CommandHandler("start", self.start))
        self._app.add_handler(pickup_handler)

        self.cache_ttl = cache_ttl

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        user = update.effective_user
        await update.message.reply_html(
            f"Добро пожаловать, {user.first_name}!",
        )

    async def pick_up(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        await update.message.reply_text(
            "Давайте подберём аккумулятор для Вашего авто.\nВведите марку и год выпуска:",
            reply_markup=self.break_reply_markup
        )
        return SEARCH

    async def search(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not (_message := update.message):
            return SEARCH
        _search_results = await search_akb(_message.text)
        _markup = self.get_options_markup(_search_results)
        await _message.reply_html(f"Результаты поиска по запросу <i>{_message.text}</i>:", reply_markup=_markup)
        return SEARCH

    async def callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        _message = update.message
        _query = update.callback_query
        await _query.answer()
        _data = _query.data
        if _data == "break":
            await _query.edit_message_text("Выберите действие в меню.", reply_markup=None)
            return ConversationHandler.END
        _parent, _items = self.unpickle(_data).values()
        _markup = self.get_options_markup(_items, parent=_parent)
        await _query.edit_message_text(f"<b>{_parent}:</b>", parse_mode=ParseMode.HTML, reply_markup=_markup)
        return SEARCH

    async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        return ConversationHandler.END

    @property
    def app(self):
        return self._app

    async def set_menu_button(self) -> None:
        await self._app.bot.set_my_commands([
            ("catalog", "Каталог"),
            ("pickup", "Подбор аккумулятора"),
        ])
        await self._app.bot.set_chat_menu_button()

    async def set_webhook(self) -> None:
        await self._app.bot.set_webhook(
            f"{API_URL}/update", secret_token=settings.TELEGRAM_BOT_WEBHOOK_SECRET_TOKEN)

    @property
    def break_button(self):
        return InlineKeyboardButton("Завершить подбор", callback_data="break")

    @property
    def break_reply_markup(self):
        return InlineKeyboardMarkup([[self.break_button]])

    def get_options_markup(self, items: list, parent: str = None):
        def extract_name(x):
            return x.get("full_name", x["name"])

        def full_name(x):
            return " - ".join(y for y in (parent, extract_name(x)) if y)

        def extract_battery(x):
            _full_name = full_name(x)
            if battery_params := x.get("battery_params"):
                url_params = {**get_url_params(battery_params), "search_for": _full_name}
                return dict(url=f"https://акб-анапа.рф/catalog?{urlencode(url_params)}")

            try:
                items = next({key: x[key]} for key in ("generations", "years", "engines") if key in x)
                return dict(callback_data=self.pickle(dict(
                    parent=_full_name,
                    **items
                )))
            except StopIteration:
                return dict(callback_data="break")

        def option_button(x):
            return InlineKeyboardButton(extract_name(x), **extract_battery(x))

        return InlineKeyboardMarkup([
            *[[option_button(x)] for x in items[:12]],
            [self.break_button]
        ])

    def pickle(self, data):
        key = str(uuid4())
        pickled_data = orjson.dumps(data)
        redis_client.set(key, pickled_data, ex=self.cache_ttl)
        return key

    def unpickle(self, key):
        if pickled_data := redis_client.get(key):
            redis_client.delete(key)
            return orjson.loads(pickled_data)
        else:
            return key
