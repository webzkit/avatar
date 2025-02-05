from fastcrud import FastCRUD
from schemas.geography.country import (
    CountryGeographyCreateInternal,
    CountryGeographyUpdate,
    CountryGeographyUpdateInternal,
    CountryGeographyDelete,
)
from models.geography.country import CountryGeographyModel

CountryCRUD = FastCRUD[
    CountryGeographyModel,
    CountryGeographyCreateInternal,
    CountryGeographyUpdate,
    CountryGeographyUpdateInternal,
    CountryGeographyDelete,
]

country_geography_curd = CountryCRUD(CountryGeographyModel)
