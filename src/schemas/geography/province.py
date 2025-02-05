from datetime import datetime
from typing import Annotated, Optional
from pydantic import BaseModel, ConfigDict, Field
from db.schemas import TimestampSchema, PersistentDeletion
from schemas.owner import UserRelationship
from schemas.geography.country import CountryGeographyRelationship


class ProvinceGeographyBase(BaseModel):
    name: Annotated[str, Field(examples=["TP Hồ Chí Minh"])]
    region_code: Annotated[str, Field(examples=["VN-SG"])]
    geography_country_id: Annotated[int, Field(examples=[1])]


class ProvinceGeography(TimestampSchema, PersistentDeletion, ProvinceGeographyBase):
    pass


class ProvinceGeographyRead(ProvinceGeographyBase):
    id: int
    created_at: datetime
    created_by: int

    country: CountryGeographyRelationship
    owner: Optional[UserRelationship] = None


class ProvinceGeographyRelationship(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: Optional[str] = None


class ProvinceGeographyCreate(ProvinceGeographyBase):
    pass


class ProvinceGeographyCreateInternal(ProvinceGeographyBase):
    created_by: int


class ProvinceGeographyUpdate(BaseModel):
    name: str | None = None


class ProvinceGeographyUpdateInternal(ProvinceGeographyUpdate):
    updated_by: Optional[int] = None


class ProvinceGeographyDelete(BaseModel):
    pass
