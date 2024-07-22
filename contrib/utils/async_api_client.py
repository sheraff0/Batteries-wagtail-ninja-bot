import re
import aiohttp
from asgiref.sync import async_to_sync
from dataclasses import dataclass, field
from enum import StrEnum, auto
from functools import wraps


class HttpMethods(StrEnum):
    GET = auto()
    POST = auto()
    DELETE = auto()


@dataclass
class AsyncClient:
    api_url: str
    default_headers: dict | None = field(default_factory=dict)
    timeout: int = 10

    def __post_init__(self):
        self.host, self.path = re.match(r"(https?://[^/]+)(.*)", self.api_url).groups()
        self.session = aiohttp.ClientSession(self.host)

    async def request(self,
        endpoint: str = "",
        method: HttpMethods = HttpMethods.GET,
        params=dict(),
        headers=dict(),
        cookies=dict(),
        data=None,
        json=None,
        result_method: str = "json",
        timeout=None,
        log=False,
    ):
        if log:
            print(data)
        print("Querying API: {method} - {_cyan}{endpoint}{_end} ? {_yellow}{params} : {data}{_end}".format(**{
            "method": (method or "get").upper(),
            "endpoint": endpoint,
            "params": params,
            "data": data or json or {},
            "_cyan": "\033[96m\033[3m",
            "_yellow": "\033[93m\033[3m",
            "_end": "\033[0m"
        }), flush=True)
        async with getattr(self.session, method)(
            self.path + endpoint,
            params=params,
            headers={**headers, **self.default_headers},
            cookies=cookies,
            data=data,
            json=json,
            timeout=timeout or self.timeout,
        ) as r:
            if log:
                print(r)
                try: print(await r.json())
                except: ...
            return (
                await (result_method if callable(result_method) else getattr(r, result_method))()
                if result_method
                    and str(r.status)[0] in ["2", "4"]
                else r
            )

    async def close(self):
        await self.session.close()


# Decorators

async def apply_api_client(cls, init_args, func, *args, **kwargs):
    api_client = cls(*init_args)
    try:
        kwargs.update({"client": api_client})
        res = await func(*args, **kwargs)
        await api_client.client.close()
        return res
    except Exception as e:
        await api_client.client.close()
        raise e


def async_api_client(cls):
    def __(func):
        @wraps(func)
        async def _(*args, **kwargs):
            return await apply_api_client(cls, [], func, *args, **kwargs)
        return _
    return __


def async_to_sync_api_client(cls):
    def ___(func):
        @wraps(func)
        def __(*args, **kwargs):
            @async_to_sync
            async def _():
                return await apply_api_client(cls, [], func, *args, **kwargs)
            return _()
        return __
    return ___
