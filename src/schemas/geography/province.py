from datetime import datetime
from typing import Annotated, Optional
from pydantic import BaseModel, ConfigDict, Field
from db.schemas import TimestampSchema, PersistentDeletion


class ProvinceGeographyBase(BaseModel):
    name: Annotated[str, Field(examples=["TP Hồ Chí Minh"])]


class ProvinceGeography(TimestampSchema, PersistentDeletion, ProvinceGeographyBase):
    pass


class ProvinceGeographyRead(ProvinceGeographyBase):
    id: int
    created_at: datetime


class ProvinceGeographyRelationship(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: Optional[str] = None


class ProvinceGeographyCreate(ProvinceGeographyBase):
    pass


class ProvinceGeographyCreateInternal(ProvinceGeographyCreate):
    created_by: int


class ProvinceGepgraphyUpdate(BaseModel):
    name: str | None = None


class ProvinceGeographyUpdateInternal(ProvinceGepgraphyUpdate):
    updated_at: datetime


class ProvinceGeographyDelete(BaseModel):
    pass
