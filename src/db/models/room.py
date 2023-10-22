"""Room model file."""
import datetime

import sqlalchemy as sa
from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from . import User, Base

from ...bot.structures.universe import Adventure


class Room(Base):
    """Room model."""

    name: Mapped[str] = mapped_column(
        sa.Text, unique=True, nullable=False
    )
    owner: Mapped[User] = mapped_column(
        sa.ForeignKey('user.id', ondelete='CASCADE')
    )
    participants_limit: Mapped[int] = mapped_column(
        sa.Integer, unique=False, nullable=False
    )
    participants_logged: Mapped[int] = mapped_column(sa.Integer)
    adventure: Mapped[Adventure] = mapped_column(sa.Enum(Adventure))
    room_character: Mapped[int] = mapped_column(
        sa.ForeignKey('character.id', ondelete='CASCADE'),
        unique=False,
        nullable=True,
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    password: Mapped[str] = mapped_column(sa.Text, unique=False, nullable=True)

