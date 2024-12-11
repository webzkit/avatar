from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String
from db.database import Base
from db.models import TimestampMixin, SoftDeleteMixin


class ProvinceGeographyModel(TimestampMixin, SoftDeleteMixin, Base):
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
    created_by: Mapped[int] = mapped_column(Integer)
