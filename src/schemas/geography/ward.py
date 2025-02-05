from datetime import datetime
from typing import Annotated, Optional
from pydantic import BaseModel, Field

from .district import DistrictGeographyRelationship
from .province import ProvinceGeographyRelationship
from ..owner import UserRelationship


class WardGeographyBase(BaseModel):
    name: Annotated[str, Field(examples=["Phuong 1"])]
    geography_district_id: Annotated[int, Field(examples=[1])]


class WardGeographyRead(WardGeographyBase):
    id: int
    created_at: datetime
    district: DistrictGeographyRelationship
    province: ProvinceGeographyRelationship
    created_by: int

    owner: Optional[UserRelationship] = None


class WardGeographyCreate(WardGeographyBase):
    pass


class WardGeographyCreateInternal(WardGeographyBase):
    created_by: int


class WardGeographyUpdate(BaseModel):
    name: str | None = None


class WardGeographyUpdateInternal(WardGeographyUpdate):
    updated_by: Optional[int] = None


class WardGeographyDelete(BaseModel):
    pass
