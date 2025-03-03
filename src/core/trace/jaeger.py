import asyncio
import functools
from typing import Any
from collections.abc import Callable
from fastapi import HTTPException, Request, Response, status

from opentelemetry import trace
from opentelemetry.propagate import extract
from opentelemetry.trace.status import Status, StatusCode


def tracing() -> Callable:
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        async def inner(request: Request, *args: Any, **kwargs) -> Response:
            context = extract(request.headers)
            print(context)
            print(__name__)
            tracer = trace.get_tracer(__name__)
            with tracer.start_as_current_span(
                "process_request", context=context
            ) as span:
                try:
                    span.set_attributes(
                        {"endpoint": "/check_health", "processing.type": "standard"}
                    )

                    await asyncio.sleep(1)
                    result = await func(request, *args, **kwargs)

                    span.set_attributes(
                        {"processing.success": True, "result.size": len(str(result))}
                    )
                except Exception as e:
                    span.set_status(Status(StatusCode.ERROR))
                    span.record_exception(e)

                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Internal Server Error",
                    )

            return result

        return inner

    return wrapper
