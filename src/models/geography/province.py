from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from db.database import Base
from db.models import TimestampMixin, SoftDeleteMixin, OwnerMixin


class ProvinceGeographyModel(OwnerMixin, TimestampMixin, SoftDeleteMixin, Base):
    __tablename__ = "geography_provinces"

    id: Mapped[int] = mapped_column(
        "id",
        autoincrement=True,
        nullable=False,
        unique=True,
        primary_key=True,
        init=False,
    )

    name: Mapped[str] = mapped_column(String(50), nullable=False)
