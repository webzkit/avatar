from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.database import Base
from db.models import OwnerMixin, SoftDeleteMixin, TimestampMixin, UUIDMixin
from models.avatar_sector import AvatarSectorModel
from models.sector import SectorModel


class AvatarModel(UUIDMixin, OwnerMixin, TimestampMixin, SoftDeleteMixin, Base):
    __tablename__ = "avatars"

    id: Mapped[int] = mapped_column(
        "id",
        autoincrement=True,
        nullable=False,
        unique=True,
        primary_key=True,
        init=False,
    )
    email: Mapped[str] = mapped_column(String(100), nullable=True)
    phone: Mapped[str] = mapped_column(String(15), nullable=True)
    firstname: Mapped[str] = mapped_column(String(50), nullable=False)
    lastname: Mapped[str] = mapped_column(String(50), nullable=False)
    is_kol: Mapped[bool] = mapped_column(Boolean, default=False)

    # sectors = relationship(SectorModel, secondary="avatar_sectors")
