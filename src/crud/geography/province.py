from fastcrud import FastCRUD
from schemas.geography.province import (
    ProvinceGeographyCreateInternal,
    ProvinceGepgraphyUpdate,
    ProvinceGeographyUpdateInternal,
    ProvinceGeographyDelete,
)
from models.geography.province import ProvinceGeographyModel

CRUDGroup = FastCRUD[
    ProvinceGeographyModel,
    ProvinceGeographyCreateInternal,
    ProvinceGepgraphyUpdate,
    ProvinceGeographyUpdateInternal,
    ProvinceGeographyDelete,
]

province_geography_curd = CRUDGroup(ProvinceGeographyModel)
