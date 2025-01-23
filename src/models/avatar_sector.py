from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from db.database import Base


class AvatarSectorModel(Base):
    __tablename__ = "avatar_sectors"

    id: Mapped[int] = mapped_column(
        "id",
        autoincrement=True,
        nullable=False,
        unique=True,
        primary_key=True,
        init=False,
    )

    avatar_id: Mapped[int] = mapped_column(
        ForeignKey("avatars.id"), index=True, default=1
    )

    sector_id: Mapped[int] = mapped_column(
        ForeignKey("sectors.id"), index=True, default=1
    )
