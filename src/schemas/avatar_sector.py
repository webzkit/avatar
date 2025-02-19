from typing import Any, List
from pydantic import BaseModel, computed_field


class AvatarSectorBase(BaseModel):
    avatar_id: int
    sector_id: int


class AvatarSectors(BaseModel):
    avatar_id: int
    sectors: Any

    @computed_field
    @property
    def data(self) -> List[AvatarSectorBase]:
        sectors = []
        for sector in self.sectors:
            sectors.append({"avatar_id": self.avatar_id, "sector_id": sector})

        return sectors


class AvatarSectorRead(AvatarSectorBase):
    pass


class AvatarSectorCreate(AvatarSectorBase):
    pass


class AvatarSectorCreateInternal(AvatarSectorBase):
    pass


class AvatarSectorUpdate(BaseModel):
    pass


class AvatarSectorUpdateInternal(AvatarSectorUpdate):
    pass


class AvatarSectorDelete(BaseModel):
    pass
