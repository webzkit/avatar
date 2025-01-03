import functools
import json
import re
from collections.abc import Callable
from typing import Any

from fastapi import Request, Response
from fastapi.encoders import jsonable_encoder
from redis.asyncio import ConnectionPool, Redis

from ..exceptions.cache_exception import (
    CacheIdentificationInferenceError,
    InvalidRequestError,
    MissingClientError,
)

pool: ConnectionPool | None = None
client: Redis | None = None


def _infer_resource_id(
    kwargs: dict[str, Any], resource_id_type: type | tuple[type, ...]
) -> int | str:
    resource_id: int | str | None = None
    for arg_name, arg_value in kwargs.items():
        if isinstance(arg_value, resource_id_type):
            if (resource_id_type is int) and ("id" in arg_name):
                resource_id = arg_value

            elif (resource_id_type is int) and ("id" not in arg_name):
                pass

            elif resource_id_type is str:
                resource_id = arg_value

    if resource_id is None:
        raise CacheIdentificationInferenceError

    return resource_id


def _extract_data_inside_brackets(input_string: str) -> list[str]:
    data_inside_brackets = re.findall(r"{(.*?)}", input_string)

    return data_inside_brackets


def _construct_data_dict(
    data_inside_brackets: list[str], kwargs: dict[str, Any]
) -> dict[str, Any]:
    data_dict = {}
    for key in data_inside_brackets:
        data_dict[key] = kwargs[key]
    return data_dict


def _format_prefix(prefix: str, kwargs: dict[str, Any]) -> str:
    data_inside_brackets = _extract_data_inside_brackets(prefix)
    data_dict = _construct_data_dict(data_inside_brackets, kwargs)
    formatted_prefix = prefix.format(**data_dict)
    return formatted_prefix


def _format_extra_data(
    to_invalidate_extra: dict[str, str], kwargs: dict[str, Any]
) -> dict[str, Any]:
    formatted_extra = {}
    for prefix, id_template in to_invalidate_extra.items():
        formatted_prefix = _format_prefix(prefix, kwargs)
        id = _extract_data_inside_brackets(id_template)[0]
        formatted_extra[formatted_prefix] = kwargs[id]

    return formatted_extra


async def _delete_keys_by_pattern(pattern: str) -> None:
    if client is None:
        raise MissingClientError

    cursor = -1
    while cursor != 0:
        cursor, keys = await client.scan(cursor, match=pattern, count=100)
        if keys:
            await client.delete(*keys)


def create_or_read_cache(
    key_prefix: str,
) -> Callable:
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        async def inner(request: Request, *args: Any, **kwargs: Any) -> Response:
            if client is None:
                raise MissingClientError

            result = await func(request, *args, **kwargs)
            print(result)
            if request.method == "GET":
                cache_key = f"{key_prefix}:1"
                cached_data = await client.get(cache_key)

                if cached_data:
                    result_cache = json.loads(cached_data.decode())
                    result["data"]["extends"] = {"user": result_cache["data"]}

                result = await func(request, *args, **kwargs)

            return result

        return inner

    return wrapper
