import orjson
import redis

from django.conf import settings

from pydantic import BaseModel
from contrib.common.pydantic import json_clean

redis_client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
redis_client.flushdb()


def get_key(coro, args, kwargs, with_args: bool = True):
    _key = orjson.dumps(dict(
        testing_mode=settings.TESTING_MODE,
        coro=coro.__name__,
        **(dict(
            args=[json_clean(v) if _dump else v for v in args if (
                _dump := issubclass(type(v), BaseModel)) is not None],
            **{k: json_clean(v) if _dump else v for k, v in kwargs.items() if (
                _dump := issubclass(type(v), BaseModel)) is not None}
        ) if with_args else {}),
    ))
    return _key
