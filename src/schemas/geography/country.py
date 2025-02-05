from datetime import datetime
from typing import Annotated, Optional
from pydantic import BaseModel, ConfigDict, Field
from db.schemas import TimestampSchema, PersistentDeletion
from schemas.owner import UserRelationship


class CountryGeographyBase(BaseModel):
    name: Annotated[str, Field(examples=["Viet Nam"])]
    region_code: Annotated[str, Field(examples=["VN"])]


class CountryGeography(TimestampSchema, PersistentDeletion, CountryGeographyBase):
    pass


class CountryGeographyRead(CountryGeographyBase):
    id: int
    created_at: datetime
    created_by: int

    owner: Optional[UserRelationship] = None


class CountryGeographyRelationship(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: Optional[str] = None


class CountryGeographyCreate(CountryGeographyBase):
    pass


class CountryGeographyCreateInternal(CountryGeographyBase):
    created_by: int


class CountryGeographyUpdate(BaseModel):
    name: str | None = None


class CountryGeographyUpdateInternal(CountryGeographyUpdate):
    updated_by: Optional[int] = None


class CountryGeographyDelete(BaseModel):
    pass
