from ..base import CRUDBase

from models.locations.district import DistrictModel
from schemas.location.district import CreatePlaceDistrictSchema, UpdatePlaceDistrictSchema


class PlaceDistrictCRUD(CRUDBase[DistrictModel, CreatePlaceDistrictSchema, UpdatePlaceDistrictSchema]):
    pass


place_district_crud = PlaceDistrictCRUD(DistrictModel)
