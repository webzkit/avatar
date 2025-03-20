from config import settings
from core.consul.discover_service import discover_service


OWNER_RELATE = {
    "service_host": discover_service(settings.APIGATEWAY_SERVICE_NAME),
    "service_path": settings.OWNER_PATH,
    "key_schema": settings.OWNER_SCHEMA,
    "key_relate": "created_by",
    "key_prefix": "user:result",
}
