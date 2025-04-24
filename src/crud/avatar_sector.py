from typing import Any, List
from fastcrud import FastCRUD
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.avatar_sector import (
    AvatarSectorCreateInternal,
    AvatarSectors,
)
from models.avatar_sector import AvatarSectorModel


crud = FastCRUD(AvatarSectorModel)
model = crud.model


async def deleteOrCreated(db: AsyncSession, object: AvatarSectors) -> Any:
    create_data: List[model] = []
    if not object.sectors:
        return

    try:
        stm = delete(model).where(model.avatar_id == object.avatar_id)
        await db.execute(stm)

        for sector in object.sectors:
            obj = AvatarSectorCreateInternal(
                avatar_id=object.avatar_id, sector_id=sector
            ).model_dump()

            # init
            db_object: model = crud.model(**obj)
            create_data.append(db_object)

        db.add_all(create_data)
        await db.commit()
    except:
        await db.rollback()
    finally:
        await db.close()

    return create_data
