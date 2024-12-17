from fastcrud import FastCRUD
from schemas.geography.ward import (
    WardGeographyCreateInternal,
    WardGepgraphyUpdate,
    WardGeographyUpdateInternal,
    WardGeographyDelete,
)
from models.geography.ward import WardGeographyModel

WardCRUD = FastCRUD[
    WardGeographyModel,
    WardGeographyCreateInternal,
    WardGepgraphyUpdate,
    WardGeographyUpdateInternal,
    WardGeographyDelete,
]

ward_geography_curd = WardCRUD(WardGeographyModel)
