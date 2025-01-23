from typing import Any
from fastcrud import FastCRUD
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.geography.district import (
    DistrictGeographyCreateInternal,
    DistrictGepgraphyUpdate,
    DistrictGeographyUpdateInternal,
    DistrictGeographyDelete,
    DistrictGeographyRead as Read,
)
from models.geography.district import DistrictGeographyModel
from schemas.geography.province import ProvinceGeographyRelationship
from models.geography.province import ProvinceGeographyModel as JoinModel

DistrictCRUD = FastCRUD[
    DistrictGeographyModel,
    DistrictGeographyCreateInternal,
    DistrictGepgraphyUpdate,
    DistrictGeographyUpdateInternal,
    DistrictGeographyDelete,
]
from core.paginated import compute_offset

district_geography_curd = DistrictCRUD(DistrictGeographyModel)

JOIN_PREFIX = "province_"


async def get_multi(db: AsyncSession, page: int = 1, items_per_page: int = 100) -> Any:
    return await district_geography_curd.get_multi_joined(
        db=db,
        offset=compute_offset(page, items_per_page),
        limit=items_per_page,
        schema_to_select=Read,
        join_model=JoinModel,  # pyright: ignore
        join_prefix=JOIN_PREFIX,
        join_schema_to_select=ProvinceGeographyRelationship,
        is_deleted=False,
        nest_joins=True,
    )


async def get_by_id(db: AsyncSession, id: int) -> Any:
    return await district_geography_curd.get_joined(
        db=db,
        schema_to_select=Read,
        id=id,
        is_deleted=False,
        join_model=JoinModel,  # pyright: ignore
        join_prefix=JOIN_PREFIX,
        join_schema_to_select=ProvinceGeographyRelationship,
        nest_joins=True,
    )
