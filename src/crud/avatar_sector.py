from fastcrud import FastCRUD
from schemas.avatar_sector import (
    AvatarSectorCreateInternal,
    AvatarSectorUpdate,
    AvatarSectorUpdateInternal,
    AvatarSectorDelete,
)
from models.avatar_sector import AvatarSectorModel

CRUD = FastCRUD[
    AvatarSectorModel,
    AvatarSectorCreateInternal,
    AvatarSectorUpdate,
    AvatarSectorUpdateInternal,
    AvatarSectorDelete,
]

crud = CRUD(AvatarSectorModel)
