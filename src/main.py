from fastapi import Request
from starlette.middleware.cors import CORSMiddleware
from typing import Any, Dict
from config import settings
from apis.api import api_router
from core.setup import create_application
from middlewares.metrics import setting_otlp

# from core.monitors.logger import Logger

# logger = Logger(__name__)

# Init application
app = create_application(router=api_router, settings=settings)


# Setting openTelemetry exporter
setting_otlp(app, settings.APP_NAME, f"{settings.OTLP_GRPC_ENDPOINT}")
print(settings.APP_NAME)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        # allow_origins=[str(origin)
        #               for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.get("/")
async def home(request: Request) -> Any:
    result: Dict[Any, Any] = {
        "status": True,
        "message": f"Your {settings.APP_NAME} endpoint is working",
    }
    # logger.info(result)

    return result


@app.get("/health")
def health_status():
    return {"status": "healthy"}
