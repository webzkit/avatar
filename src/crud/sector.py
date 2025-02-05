from fastcrud import FastCRUD
from schemas.sector import (
    SectorCreateInternal,
    SectorUpdate,
    SectorUpdateInternal,
    SectorDelete,
)
from models.sector import SectorModel

SectorCRUD = FastCRUD[
    SectorModel, SectorCreateInternal, SectorUpdate, SectorUpdateInternal, SectorDelete
]

crud = SectorCRUD(SectorModel)
