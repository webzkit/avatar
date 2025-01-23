from fastcrud import FastCRUD
from schemas.geography.province import (
    ProvinceGeographyCreateInternal,
    ProvinceGeographyUpdate,
    ProvinceGeographyUpdateInternal,
    ProvinceGeographyDelete,
)
from models.geography.province import ProvinceGeographyModel

ProvinceCRUD = FastCRUD[
    ProvinceGeographyModel,
    ProvinceGeographyCreateInternal,
    ProvinceGeographyUpdate,
    ProvinceGeographyUpdateInternal,
    ProvinceGeographyDelete,
]

province_geography_curd = ProvinceCRUD(ProvinceGeographyModel)
