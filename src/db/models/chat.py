"""Chat model file."""
import datetime

import sqlalchemy as sa
from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from . import Base


class Chat(Base):
    """Chat model."""

    chat_id: Mapped[int] = mapped_column(
        sa.BigInteger, unique=True, nullable=False
    )
    """ Chat telegram id """
    chat_type: Mapped[str] = mapped_column(
        sa.Text, unique=False, nullable=False
    )
    """ Chat type can be either ‘private’, ‘group’, ‘supergroup’ or ‘channel’ """
    title: Mapped[str] = mapped_column(sa.Text, unique=False, nullable=True)
    """ Title of the chat """
    chat_name: Mapped[str] = mapped_column(
        sa.Text, unique=False, nullable=True
    )
    """ Telegram chat full name """
    chat_user: Mapped[int] = mapped_column(
        sa.ForeignKey('user.id', ondelete='CASCADE'),
        unique=False,
        nullable=True,
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    """ Foreign key to user (it can has effect only in private chats) """
    last_activity: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
