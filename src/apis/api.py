from fastapi import APIRouter
from .v1.geography import province, district, ward
from .v1 import sector

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

api_router.include_router(sector.router, prefix="/sectors", tags=["Avatar Sector"])
