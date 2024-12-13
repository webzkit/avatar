from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey
from db.database import Base
from db.models import TimestampMixin, SoftDeleteMixin, OwnerMixin


class DistrictGeographyModel(OwnerMixin, TimestampMixin, SoftDeleteMixin, Base):
    __tablename__ = "geography_districts"

    id: Mapped[int] = mapped_column(
        "id",
        autoincrement=True,
        nullable=False,
        unique=True,
        primary_key=True,
        init=False,
    )

    name: Mapped[str] = mapped_column(String(50), nullable=False)

    geography_provinces_id: Mapped[int] = mapped_column(
        ForeignKey("geography_provinces.id"), index=True, default=1
    )
