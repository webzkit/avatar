from typing import Any, List
from fastcrud import FastCRUD
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.avatar_sector import (
    AvatarSectorCreateInternal,
    AvatarSectorUpdate,
    AvatarSectorUpdateInternal,
    AvatarSectorDelete,
    AvatarSectorBase,
)
from models.avatar_sector import AvatarSectorModel


CRUD = FastCRUD[
    AvatarSectorModel,
    AvatarSectorCreateInternal,
    AvatarSectorUpdate,
    AvatarSectorUpdateInternal,
    AvatarSectorDelete,
]

crud = CRUD(AvatarSectorModel)


async def updateOrCreate(db: AsyncSession, objects: Any, id_deleted: int) -> Any:
    create_data: List[AvatarSectorBase] = []
    if not objects:
        return

    try:
        stm = delete(AvatarSectorModel).where(AvatarSectorModel.avatar_id == id_deleted)
        await db.execute(stm)

        for object in objects:
            db_object: Any = crud.model(**object)
            create_data.append(db_object)

        db.add_all(create_data)
        await db.commit()
    except:
        print("erro")
        await db.rollback()
    finally:
        await db.close()

    return create_data
