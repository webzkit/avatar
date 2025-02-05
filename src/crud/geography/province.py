from typing import Any
from fastcrud import FastCRUD
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.geography.province import (
    ProvinceGeographyCreateInternal,
    ProvinceGeographyUpdate,
    ProvinceGeographyUpdateInternal,
    ProvinceGeographyDelete,
    ProvinceGeographyRead as Read,
)
from models.geography.province import ProvinceGeographyModel
from models.geography.country import CountryGeographyModel as JoinModel
from schemas.geography.country import CountryGeographyRelationship
from core.paginated import compute_offset


ProvinceCRUD = FastCRUD[
    ProvinceGeographyModel,
    ProvinceGeographyCreateInternal,
    ProvinceGeographyUpdate,
    ProvinceGeographyUpdateInternal,
    ProvinceGeographyDelete,
]

province_geography_curd = ProvinceCRUD(ProvinceGeographyModel)
JOIN_PREFIX = "country_"


async def get_multi(db: AsyncSession, page: int = 1, items_per_page: int = 100) -> Any:
    return await province_geography_curd.get_multi_joined(
        db=db,
        offset=compute_offset(page, items_per_page),
        limit=items_per_page,
        schema_to_select=Read,
        join_model=JoinModel,  # pyright: ignore
        join_prefix=JOIN_PREFIX,
        join_schema_to_select=CountryGeographyRelationship,
        is_deleted=False,
        nest_joins=True,
    )


async def get_by_id(db: AsyncSession, id: int) -> Any:
    return await province_geography_curd.get_joined(
        db=db,
        schema_to_select=Read,
        id=id,
        is_deleted=False,
        join_model=JoinModel,  # pyright: ignore
        join_prefix=JOIN_PREFIX,
        join_schema_to_select=CountryGeographyRelationship,
        nest_joins=True,
    )
