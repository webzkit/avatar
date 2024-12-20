from datetime import datetime
from typing import Annotated, Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field
from db.schemas import TimestampSchema, PersistentDeletion

from .district import DistrictGeographyRelationship
from .province import ProvinceGeographyRelationship


class WardGeographyBase(BaseModel):
    name: Annotated[str, Field(examples=["Phuong 1"])]
    geography_district_id: Annotated[int, Field(examples=[1])]


class WardGeography(TimestampSchema, PersistentDeletion, WardGeographyBase):
    pass


class WardGeographyRead(WardGeographyBase):
    id: int
    created_at: datetime
    district: DistrictGeographyRelationship
    province: ProvinceGeographyRelationship
    created_by: int

    extends: Optional[Dict[str, Any]] = None


class WardGeographyCreate(WardGeographyBase):
    pass


class WardGeographyCreateInternal(WardGeographyBase):
    created_by: int


class WardGepgraphyUpdate(BaseModel):
    name: str | None = None


class WardGeographyUpdateInternal(WardGepgraphyUpdate):
    updated_by: Optional[int] = None


class WardGeographyDelete(BaseModel):
    pass
