from fastcrud import FastCRUD
from schemas.geography.district import (
    DistrictGeographyCreateInternal,
    DistrictGepgraphyUpdate,
    DistrictGeographyUpdateInternal,
    DistrictGeographyDelete,
)
from models.geography.district import DistrictGeographyModel

DistrictCRUD = FastCRUD[
    DistrictGeographyModel,
    DistrictGeographyCreateInternal,
    DistrictGepgraphyUpdate,
    DistrictGeographyUpdateInternal,
    DistrictGeographyDelete,
]

district_geography_curd = DistrictCRUD(DistrictGeographyModel)
