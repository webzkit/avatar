from datetime import datetime
from typing import Annotated, Any, List, Optional
from pydantic import BaseModel, EmailStr, Field
from schemas.owner import UserRelationship


class AvatarBase(BaseModel):
    email: Optional[EmailStr] = Field(default=None)
    phone: Optional[str] = Field(
        default=None, min_length=10, max_length=15, pattern=r"^\d*$"
    )
    firstname: Annotated[str, Field(default="firstName")]
    lastname: Annotated[str, Field(default="lastName")]
    is_kol: Annotated[bool, Field(default=False)]


class AvatarRead(AvatarBase):
    id: int
    created_at: datetime
    created_by: int

    owner: Optional[UserRelationship] = None


class AvatarCreate(AvatarBase):
    sectors: Annotated[List[Any], Field(default=[1])]


class AvatarCreateInternal(AvatarBase):
    created_by: int


class AvatarUpdate(BaseModel):
    email: str | None = None


class AvatarUpdateInternal(AvatarUpdate):
    updated_by: Optional[int] = None


class AvatarDelete(BaseModel):
    pass
