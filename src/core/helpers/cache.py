import functools
import json
from collections.abc import Callable
from typing import Any, Dict, List, Optional

from fastapi import Request, Response
from redis.asyncio import ConnectionPool, Redis

from ..exceptions.cache_exception import (
    MissingClientError,
)

from core.http.client import call_to_service

pool: ConnectionPool | None = None
client: Redis | None = None


def get_service_related(
    key_prefix: str, related: Optional[List[dict]] = None
) -> Callable:
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        async def inner(request: Request, *args: Any, **kwargs: Any) -> Response:
            if client is None:
                raise MissingClientError

            result = await func(request, *args, **kwargs)

            if not related:
                return result

            if request.method == "GET":
                for relate in related:
                    await get_relate(relate, id=1)

                cache_key = f"{key_prefix}:1"
                cached_data = await client.get(cache_key)

                if cached_data:
                    result_cache = json.loads(cached_data.decode())
                    result["data"]["owner"] = result_cache["data"]

                else:
                    url = "http://engine:8000/api/v1/users/1"
                    resp_data, status_code_from_service = await call_to_service(
                        request=request,
                        url=url,
                        method=request.method,
                        payload={},
                        service_headers=request.headers,
                        request_param={},
                    )
                    result["data"]["owner"] = resp_data["data"]

            return result

        return inner

    return wrapper


async def get_relate(relate: Any, id: int):
    cache_key = f"{relate.get('key_prefix')}:{id}"
    print(cache_key)
