from config import settings


OWNER_RELATE = {
    "service_host": settings.API_GATEWAY_SERVICE_URL,
    "service_path": settings.OWNER_PATH,
    "key_schema": settings.OWNER_SCHEMA,
    "key_relate": "created_by",
    "key_prefix": "user:result",
}
