from datetime import datetime
from typing import Annotated, Optional
from pydantic import BaseModel, ConfigDict, Field
from schemas.owner import UserRelationship


class SectorBase(BaseModel):
    name: Annotated[str, Field(examples=["Social"])]


class SectorRead(SectorBase):
    id: int
    created_at: datetime
    created_by: int

    owner: Optional[UserRelationship] = None


class SectorRelationship(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: Optional[str] = None


class SectorCreate(SectorBase):
    pass


class SectorCreateInternal(SectorBase):
    created_by: int


class SectorUpdate(BaseModel):
    name: str | None = None


class SectorUpdateInternal(SectorUpdate):
    updated_by: Optional[int] = None


class SectorDelete(BaseModel):
    pass
