from fastapi import APIRouter
from .v1.geography import province, district, ward

api_router = APIRouter()

api_router.include_router(
    province.router, prefix="/geographies/provinces", tags=["Geograpphy Province"]
)

api_router.include_router(
    district.router, prefix="/geographies/districts", tags=["Geography District"]
)

api_router.include_router(
    ward.router, prefix="/geographies/wards", tags=["Geography Ward"]
)
