from datetime import datetime
from typing import Annotated, Optional
from pydantic import BaseModel, ConfigDict, Field

from .province import ProvinceGeographyRelationship
from ..owner import UserRelationship


class DistrictGeographyBase(BaseModel):
    name: Annotated[str, Field(examples=["Quận 1"])]
    geography_province_id: Annotated[int, Field(examples=[1])]


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


class DistrictGeographyUpdate(BaseModel):
    name: str | None = None


class DistrictGeographyUpdateInternal(DistrictGeographyUpdate):
    updated_by: Optional[int] = None


class DistrictGeographyDelete(BaseModel):
    pass
