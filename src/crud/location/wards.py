from ..base import CRUDBase

from models.locations.wards import WardsModel
from schemas.location.wards import CreatePlaceWardsSchema, UpdatePlaceWardsSchema


class PlaceWardsCRUD(CRUDBase[WardsModel, CreatePlaceWardsSchema, UpdatePlaceWardsSchema]):
    pass


place_wards_crud = PlaceWardsCRUD(WardsModel)
