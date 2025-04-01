from config import settings


OWNER_RELATE = {
    "service_name": settings.APIGATEWAY_SERVICE_NAME,
    "service_path": settings.OWNER_PATH,
    "key_schema": settings.OWNER_SCHEMA,
    "key_relate": "created_by",
    "key_prefix": "user:result",
}
