from ..base import CRUDBase

from models.locations.province import ProvinceModel
from schemas.location.province import CreatePlaceProvinceSchema, UpdatePlaceProvinceSchema


class PlaceProvinceCRUD(CRUDBase[ProvinceModel, CreatePlaceProvinceSchema, UpdatePlaceProvinceSchema]):
    pass


place_province_crud = PlaceProvinceCRUD(ProvinceModel)
