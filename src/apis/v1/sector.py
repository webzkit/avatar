from typing import Annotated, Any, Union
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from crud.sector import sector_curd as crud
from core import message
from fastapi.responses import JSONResponse
from core.paginated import PaginatedListResponse, compute_offset, paginated_response
from schemas.sector import (
    SectorRead as Read,
    SectorCreate as Create,
    SectorCreateInternal as CreateInternal,
    SectorUpdate as Update,
    SectorUpdateInternal as UpdateInternal,
)
from apis.deps import async_get_db
from core.paginated import (
    paginated_response,
    compute_offset,
    PaginatedListResponse,
    SingleResponse,
)
from core.caches.relate import get_service_relate, get_service_relates
from core.caches.define import OWNER_RELATE


router = APIRouter()


@router.get(
    "",
    response_model=PaginatedListResponse[Read],
    status_code=status.HTTP_200_OK,
)
@get_service_relates(related=[OWNER_RELATE])
async def gets(
    request: Request,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    page: int = 1,
    items_per_page: int = 100,
) -> Any:
    users_data = await crud.get_multi(
        db=db,
        offset=compute_offset(page, items_per_page),
        limit=items_per_page,
        schema_to_select=Read,
        is_deleted=False,
    )

    response: dict[str, Any] = paginated_response(
        crud_data=users_data, page=page, items_per_page=items_per_page
    )

    return response


@router.get(
    "/{id}", response_model=SingleResponse[Read], status_code=status.HTTP_200_OK
)
@get_service_relate(related=[OWNER_RELATE])
async def get(
    request: Request,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    id: int,
) -> Any:
    result = await crud.get(db=db, schema_to_select=Read, id=id, is_deleted=False)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=message.ITEM_NOT_FOUND
        )

    return {"data": result}


@router.post("", status_code=status.HTTP_201_CREATED)
async def create(
    request: Request,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    data_request: Create,
) -> Response:
    exists = await crud.exists(db=db, name=data_request.name)
    if exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=message.ITEM_ALREADY_EXISTS
        )

    data_internal = CreateInternal(**await request.json())

    await crud.create(db=db, object=data_internal)
    return JSONResponse(
        status_code=status.HTTP_200_OK, content={"detail": message.CREATE_SUCCEED}
    )


@router.put("/{id}", status_code=status.HTTP_200_OK)
async def update(
    request: Request,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    id: int,
    data_request: Update,
) -> Response:
    exists = await crud.exists(db=db, id=id)

    if not exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=message.ITEM_NOT_FOUND
        )

    data_internal = UpdateInternal(**await request.json())
    await crud.update(db=db, object=data_internal, id=id)

    return JSONResponse(
        status_code=status.HTTP_200_OK, content={"detail": message.UPDATE_SUCCEED}
    )


@router.delete("/soft/{id}", status_code=status.HTTP_200_OK)
async def soft_delete(
    id: int,
    db: Annotated[AsyncSession, Depends(async_get_db)],
) -> Response:
    result: Union[Read, Any] = await crud.get(db=db, schema_to_select=Read, id=id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=message.ITEM_NOT_FOUND
        )

    await crud.delete(db=db, id=id)

    return JSONResponse(
        status_code=status.HTTP_200_OK, content={"detail": message.DELETE_SUCCEED}
    )


@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete(
    id: int,
    db: Annotated[AsyncSession, Depends(async_get_db)],
) -> Response:
    result: Union[Read, Any] = await crud.get(db=db, schema_to_select=Read, id=id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=message.ITEM_NOT_FOUND
        )

    await crud.db_delete(db=db, id=id)

    return JSONResponse(
        status_code=status.HTTP_200_OK, content={"detail": message.DELETE_SUCCEED}
    )
