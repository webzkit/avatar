from datetime import datetime
from typing import Annotated, Any, List, Optional
from pydantic import BaseModel, EmailStr, Field, computed_field


class AvatarSectorBase(BaseModel):
    avatar_id: int
    sector_id: int


class AvatarSectorCreateInternal(BaseModel):
    avatar: int
    sectors: Any

    @computed_field
    @property
    def data(self) -> Any:
        sectors = []
        for sector in self.sectors:
            sectors.append({"avatar_id": self.avatar, "sector_id": sector})

        return sectors


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
