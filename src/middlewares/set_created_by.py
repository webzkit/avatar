from typing import Any
from fastapi import FastAPI, HTTPException, Request, Response, status
from fastapi.responses import JSONResponse
from starlette.types import Message
import json
from core.helpers.utils import parse_query_str
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint


class MakeCreatedByMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI) -> None:
        super().__init__(app)

    async def set_body(self, request: Request) -> Any:
        receive_ = await request._receive()
        body = receive_.get("body")
        body_string: str = body.decode("utf-8")  # pyright: ignore
        data = json.loads(body_string)

        try:
            data["created_by"] = await self.get_created_by(request)
            data["updated_by"] = await self.get_created_by(request)
        except HTTPException as error:
            raise error

        async def receive() -> Message:
            receive_["body"] = json.dumps(data).encode()

            return receive_

        request._receive = receive

    async def get_body(self, request: Request) -> Any:
        body = await request.body()
        await self.set_body(request)

        return body

    async def get_created_by(self, request: Request) -> Response | Any:
        request_init_data = request.headers.get("request-init-data")
        if request_init_data is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid request init data",
            )

        current_user = parse_query_str(request_init_data)
        return current_user.get("id")

    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        if request.method in ["POST", "PUT"]:
            try:
                await self.set_body(request)
            except HTTPException as error:
                print(error.status_code)
                return JSONResponse(
                    status_code=error.status_code,
                    content={"detail": error.detail},
                )

        response: Response = await call_next(request)

        return response
