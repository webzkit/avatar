from fastcrud import FastCRUD
from schemas.avatar import (
    AvatarCreateInternal,
    AvatarUpdate,
    AvatarUpdateInternal,
    AvatarDelete,
)
from models.avatar import AvatarModel

CRUD = FastCRUD[
    AvatarModel, AvatarCreateInternal, AvatarUpdate, AvatarUpdateInternal, AvatarDelete
]

crud = CRUD(AvatarModel)
