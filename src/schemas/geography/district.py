from datetime import datetime
from typing import Annotated, Optional
from pydantic import BaseModel, ConfigDict, Field
from db.schemas import TimestampSchema, PersistentDeletion

from .province import ProvinceGeographyRelationship
from ..owner import UserRelationship


class DistrictGeographyBase(BaseModel):
    name: Annotated[str, Field(examples=["Quận 1"])]
    geography_province_id: Annotated[int, Field(examples=[1])]


class DistrictGeography(TimestampSchema, PersistentDeletion, DistrictGeographyBase):
    pass


class DistrictGeographyRead(DistrictGeographyBase):
    id: int
    created_at: datetime
    province: ProvinceGeographyRelationship
    created_by: int

    owner: Optional[UserRelationship] = None


class DistrictGeographyRelationship(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: Optional[str] = None


class DistrictGeographyCreate(DistrictGeographyBase):
    pass


class DistrictGeographyCreateInternal(DistrictGeographyBase):
    created_by: int


class DistrictGepgraphyUpdate(BaseModel):
    name: str | None = None


class DistrictGeographyUpdateInternal(DistrictGepgraphyUpdate):
    updated_by: Optional[int] = None


class DistrictGeographyDelete(BaseModel):
    pass
