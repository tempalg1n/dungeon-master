import datetime

import sqlalchemy as sa
from sqlalchemy import DateTime, func, orm
from sqlalchemy.orm import Mapped, mapped_column

from . import User, Base, Room


class Character(Base):
    """Character model."""

    owner_id: Mapped[User] = mapped_column(
        sa.ForeignKey('user.id', ondelete='CASCADE')
    )
    name: Mapped[str] = mapped_column(
        sa.Text, unique=False, nullable=False
    )
    room_fk: Mapped[int] = mapped_column(
        sa.ForeignKey('room.id'), unique=False, nullable=False
    )
    room: Mapped[Room] = orm.relationship(
        "Room", uselist=False, lazy='joined', foreign_keys=room_fk
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
