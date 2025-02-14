from datetime import datetime
from typing import Annotated, Any, List, Optional
from pydantic import BaseModel, EmailStr, Field


class AvatarSectorBase(BaseModel):
    avatar_id: int
    sector_id: int


class AvatarSectorCreateInternal(AvatarSectorBase):
    pass


class AvatarSectorRead(AvatarSectorBase):
    pass


class AvatarSectorCreate(AvatarSectorBase):
    pass


class AvatarSectorUpdate(BaseModel):
    pass


class AvatarSectorUpdateInternal(AvatarSectorUpdate):
    pass


class AvatarSectorDelete(BaseModel):
    pass
