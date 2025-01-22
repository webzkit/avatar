from typing import Any, Dict
import aiohttp
import async_timeout
from fastapi import HTTPException, status
from config import settings
from core.exceptions.http_exception import ServiceHttpException


async def call_to_service(
    url: str,
    method: str = "GET",
    payload: Dict = {},
    service_headers: Any = {},
    request_param: Dict = {},
):
    try:
        resp_data, status_code_from_service = await make_request(
            url=url,
            method=method.lower(),
            data=payload,
            headers=service_headers,
            params=request_param,
        )
    except aiohttp.ClientConnectorError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service Unavailable",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except aiohttp.ContentTypeError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Service error.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except ServiceHttpException as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )

    return resp_data, status_code_from_service


async def make_request(
    url: str, method: str, data: dict = {}, headers: dict = {}, params: dict = {}
):
    if not data:
        data = {}

    with async_timeout.timeout(settings.HTTP_TIMEOUT_SERVICE):
        async with aiohttp.ClientSession() as session:
            request = getattr(session, method)
            async with request(
                url, json=data, headers=headers, params=params
            ) as response:
                if response.ok:
                    data = await response.json()
                    return (data, response.status)

                res = await response.json()

                raise ServiceHttpException(res.get("detail"))
