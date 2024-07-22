from dataclasses import dataclass
from functools import wraps
import orjson

from django.apps import apps
from django.conf import settings
from django.db import models

from pydantic import BaseModel

from contrib.common.redis import redis_client, get_key


def acached(
    coro=None,
    ttl: int = 10,
    with_args: bool = True,
):
    def __(coro):
        @wraps(coro)
        async def _(*args, **kwargs):
            _reset_cache = kwargs.pop("reset_cache", False)
            _key = get_key(coro, args, kwargs, with_args=with_args)
            if _reset_cache:
                redis_client.delete(_key)
            if _value := redis_client.get(_key):
                return orjson.loads(_value)
            else:
                _value = await coro(*args, **kwargs)
                redis_client.set(_key, orjson.dumps(_value), ex=ttl)
                return _value
        return _
    return __(coro) if callable(coro) else __


@acached
async def get_model_map(app_model: str, key: str):
    Model = apps.get_model(*app_model.split("."))
    return {x[key]: str(x["pk"]) async for x in Model.objects.values("pk", key).all()}


@acached
async def get_model_object(app_model: str, key: str, code: str | int):
    _map = await get_model_map(app_model, key)
    return _map.get(code)


@dataclass
class CachedModelMap:
    model: models.Model = None
    key: str = "code"

    def __post_init__(self):
        assert self.model, "Please define model!"
        _meta = self.model._meta
        self.app_model = ".".join((_meta.app_label, _meta.object_name))

    async def __call__(self, code: str | int):
        return await get_model_object(self.app_model, self.key, code)


def amemo(key_attr: str = "checksum", ex: int = 3600):
    def __(coro):
        @wraps(coro)
        async def _(*args, **kwargs):
            res = await coro(*args, **kwargs)
            if issubclass(type(res), BaseModel):
                _key = getattr(res, key_attr, None)

                _reset_cache = kwargs.pop("reset_cache", False)
                if _reset_cache:
                    redis_client.delete(_key)

                if _key and not redis_client.exists(_key):
                    _value = orjson.dumps(res.model_dump(exclude_none=True))
                    redis_client.set(_key, _value, ex=ex)
            return res
        return _
    return __


def get_memo(key, Model: BaseModel):
    try:
        _value = redis_client.get(key)
        _value = orjson.loads(_value)
        return Model(**_value)
    except: ...
