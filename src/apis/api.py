from fastapi import APIRouter
from .v1.geography import province

api_router = APIRouter()

api_router.include_router(
    province.router, prefix="/geographies/provinces", tags=["Geograpgies Province"]
)
