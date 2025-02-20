from typing import Any, List
from fastcrud import FastCRUD, JoinConfig
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.avatar import (
    AvatarCreateInternal,
    AvatarUpdate,
    AvatarUpdateInternal,
    AvatarDelete,
    AvatarRead as Read,
)
from models.avatar import AvatarModel
from models.avatar_sector import AvatarSectorModel as JoinModel
from models.sector import SectorModel
from schemas.sector import SectorRelationship
from core.paginated.helper import compute_offset

CRUD = FastCRUD[
    AvatarModel, AvatarCreateInternal, AvatarUpdate, AvatarUpdateInternal, AvatarDelete
]

crud = CRUD(AvatarModel)
JOIN_PREFIX = "sectors_"
JOIN_PREFIX_MANY = "join_many"


async def get_multi(db: AsyncSession, page: int = 1, items_per_page: int = 100) -> Any:
    return await crud.get_multi_joined(
        db=db,
        offset=compute_offset(page, items_per_page),
        limit=items_per_page,
        schema_to_select=Read,
        is_deleted=False,
        joins_config=[
            JoinConfig(
                model=JoinModel,
                join_on=crud.model.id == JoinModel.avatar_id,
                join_prefix=JOIN_PREFIX_MANY,
                join_type="left",
                relationship_type="one-to-many",
            ),
            JoinConfig(
                model=SectorModel,
                join_on=JoinModel.sector_id == SectorModel.id,
                join_prefix=JOIN_PREFIX,
                join_type="left",
                relationship_type="one-to-many",
                schema_to_select=SectorRelationship,
            ),
        ],
        nest_joins=True,
    )


async def get_by_id(db: AsyncSession, id: int) -> Any:
    return await crud.get_joined(
        db=db,
        schema_to_select=Read,
        id=id,
        is_deleted=False,
        joins_config=[
            JoinConfig(
                model=JoinModel,
                join_on=crud.model.id == JoinModel.avatar_id,
                join_prefix=JOIN_PREFIX_MANY,
                join_type="left",
                relationship_type="one-to-many",
            ),
            JoinConfig(
                model=SectorModel,
                join_on=JoinModel.sector_id == SectorModel.id,
                join_prefix=JOIN_PREFIX,
                join_type="left",
                relationship_type="one-to-many",
                schema_to_select=SectorRelationship,
            ),
        ],
        nest_joins=True,
    )
