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

CRUD = FastCRUD[
    AvatarModel, AvatarCreateInternal, AvatarUpdate, AvatarUpdateInternal, AvatarDelete
]

crud = CRUD(AvatarModel)
JOIN_PREFIX = "sectors_"
JOIN_PREFIX_MANY = "tests"


async def get_by_id(db: AsyncSession, id: int) -> Any:
    """
    test = await crud.get_joined(
        db=db,
        schema_to_select=Read,
        id=id,
        is_deleted=False,
        join_model=JoinModel,  # pyright: ignore
        join_prefix=JOIN_PREFIX,
        join_on=(crud.model.id == JoinModel.avatar_id),
        nest_joins=True,
        relationship_type="one-to-many",
    )
    """
    test = await crud.get_joined(
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
                # schema_to_select=SectorRelationship,
            ),
        ],
        nest_joins=True,
    )

    print(test)
    return test
