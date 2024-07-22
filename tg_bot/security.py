from django.conf import settings

from fastapi import Depends, HTTPException
from fastapi.security.api_key import APIKeyHeader


async def secret_token(
    token: str = Depends(APIKeyHeader(name="X-Telegram-Bot-Api-Secret-Token"))
):
    try:
        assert settings.TELEGRAM_BOT_WEBHOOK_SECRET_TOKEN == token
    except AssertionError:
        raise HTTPException(401, "Unauthorized")
