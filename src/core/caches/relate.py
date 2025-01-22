import functools
import json
from collections.abc import Callable
from typing import Any, List, Optional
from fastapi import Request, Response, status
from redis.asyncio import ConnectionPool, Redis

from ..exceptions.cache_exception import (
    MissingClientError,
)

from ..http.client import call_to_service

pool: ConnectionPool | None = None
client: Redis | None = None


def get_service_related(related: Optional[List[dict]] = None) -> Callable:
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        async def inner(request: Request, *args: Any, **kwargs: Any) -> Response:

            result = await func(request, *args, **kwargs)

            if not related:
                return result

            if request.method == "GET":
                for relate in related:
                    result_cache = await get_relate(relate, result["data"], request)
                    if result_cache:
                        result["data"][await get_key_relate_schema(relate)] = (
                            result_cache["data"]
                        )

            return result

        return inner

    return wrapper


async def get_relate(relate: Any, data: Any, request: Request) -> Any:
    cache_key = await get_cache_key(relate, data)
    if client is None:
        raise MissingClientError

    result_cache = await client.get(cache_key)
    if result_cache:
        return json.loads(result_cache.decode())

    resp_data, status_code_from_service = await call_to_service(
        request=request,
        url=await get_uri_key(relate, data),
        method=request.method,
        payload={},
        service_headers=request.headers,
        request_param={},
    )

    if status_code_from_service == status.HTTP_200_OK:
        return resp_data

    return


async def get_key_relate_schema(relate: Any):
    return relate.get("key_schema", None)


async def get_uri_key(relate: Any, data: Any):
    owner_id = data.get(relate.get("key_relate", None), None)

    return f"{relate.get('service_host')}{relate.get('service_path')}{owner_id}"


async def get_cache_key(relate: Any, data: Any):
    owner_id = data.get(relate.get("key_relate", None), None)

    return f"{relate.get('key_prefix')}:{owner_id}"
