from fastcrud import FastCRUD, JoinConfig
from sqlalchemy.ext.asyncio import AsyncSession
from models.geography.ward import WardGeographyModel
from schemas.geography.ward import (
    WardGeographyRead as Read,
)
from models.geography.ward import WardGeographyModel as Model
from models.geography.district import DistrictGeographyModel as JoinModel
from models.geography.province import ProvinceGeographyModel as JoinModelSecond
from schemas.geography.district import DistrictGeographyRelationship
from schemas.geography.province import ProvinceGeographyRelationship
from core.paginated import compute_offset


crud = FastCRUD(WardGeographyModel)


JOIN_PREFIX = "district_"
JOIN_PREFIX_SECOND = "province_"


async def get_multi(db: AsyncSession, page: int = 1, items_per_page: int = 100):
    return await crud.get_multi_joined(
        db=db,
        offset=compute_offset(page, items_per_page),
        limit=items_per_page,
        schema_to_select=Read,
        is_deleted=False,
        nest_joins=True,
        joins_config=[
            JoinConfig(
                model=JoinModel,
                join_on=Model.geography_district_id == JoinModel.id,
                join_prefix=JOIN_PREFIX,
                join_type="left",
                schema_to_select=DistrictGeographyRelationship,
            ),
            JoinConfig(
                model=JoinModelSecond,
                join_on=JoinModel.geography_province_id == JoinModelSecond.id,
                join_prefix=JOIN_PREFIX_SECOND,
                join_type="left",
                schema_to_select=ProvinceGeographyRelationship,
            ),
        ],
    )


async def get_by_id(db: AsyncSession, id: int):
    return await crud.get_joined(
        db=db,
        schema_to_select=Read,
        id=id,
        is_deleted=False,
        nest_joins=True,
        joins_config=[
            JoinConfig(
                model=JoinModel,
                join_on=Model.geography_district_id == JoinModel.id,
                join_prefix=JOIN_PREFIX,
                join_type="left",
                schema_to_select=DistrictGeographyRelationship,
            ),
            JoinConfig(
                model=JoinModelSecond,
                join_on=JoinModel.geography_province_id == JoinModelSecond.id,
                join_prefix=JOIN_PREFIX_SECOND,
                join_type="left",
                schema_to_select=ProvinceGeographyRelationship,
            ),
        ],
    )
