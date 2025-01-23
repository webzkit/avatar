from typing import Annotated, Any, Union
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from crud.geography.district import (
    district_geography_curd as crud,
    get_multi,
    get_by_id,
)
from core import message
from fastapi.responses import JSONResponse
from core.paginated import PaginatedListResponse, paginated_response
from schemas.geography.district import (
    DistrictGeographyRead as Read,
    DistrictGeographyCreate as Create,
    DistrictGeographyCreateInternal as CreateInternal,
    DistrictGepgraphyUpdate as Update,
    DistrictGeographyUpdateInternal as UpdateInternal,
)
from apis.deps import async_get_db
from core.paginated import (
    paginated_response,
    PaginatedListResponse,
    SingleResponse,
)
from core.caches.relate import get_service_relates, get_service_relate
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
    results = await get_multi(db=db, page=page, items_per_page=items_per_page)

    response: dict[str, Any] = paginated_response(
        crud_data=results, page=page, items_per_page=items_per_page
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
    result = await get_by_id(db=db, id=id)

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
