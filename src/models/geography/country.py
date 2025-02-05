from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from db.database import Base
from db.models import TimestampMixin, SoftDeleteMixin, OwnerMixin


class CountryGeographyModel(OwnerMixin, TimestampMixin, SoftDeleteMixin, Base):
    __tablename__ = "geography_countries"

    id: Mapped[int] = mapped_column(
        "id",
        autoincrement=True,
        nullable=False,
        unique=True,
        primary_key=True,
        init=False,
    )

    name: Mapped[str] = mapped_column(String(50), nullable=False)
    region_code: Mapped[str] = mapped_column(String(2), nullable=True)
