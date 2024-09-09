from fastapi import APIRouter


from .endpoints.location import province
from .endpoints.location import district
from .endpoints.location import wards


api_router = APIRouter()


api_router.include_router(
    province.router,
    prefix="/place/provinces",
    tags=["place_province"]
)

api_router.include_router(
    district.router,
    prefix="/place/districts",
    tags=["place_district"]
)

api_router.include_router(
    wards.router,
    prefix="/place/wards",
    tags=["place_wards"]
)
