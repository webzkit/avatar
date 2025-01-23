from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from db.database import Base
from db.models import OwnerMixin, SoftDeleteMixin, TimestampMixin


class SectorModel(OwnerMixin, TimestampMixin, SoftDeleteMixin, Base):
    __tablename__ = "sectors"

    id: Mapped[int] = mapped_column(
        "id",
        autoincrement=True,
        nullable=False,
        unique=True,
        primary_key=True,
        init=False,
    )

    name: Mapped[str] = mapped_column(String(50), nullable=False)
