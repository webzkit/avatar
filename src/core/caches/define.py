from config import settings


OWNER_RELATE = {
    "service_name": settings.ENGINE_SERVICE_NAME,
    "service_path": settings.OWNER_PATH,
    "key_schema": settings.OWNER_SCHEMA,
    "key_relate": "created_by",
    "key_prefix": "users:result",
}
