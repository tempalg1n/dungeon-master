"""User repository file."""
import bcrypt
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from .abstract import Repository
from ..models import Room
from ...bot.structures.universe import Adventure


class RoomRepo(Repository[Room]):
    """User repository for CRUD and other SQL queries."""

    def __init__(self, session: AsyncSession):
        """Initialize user repository as for all users or only for one user."""
        super().__init__(type_model=Room, session=session)

    async def new(
            self,
            owner_id: int,
            name: str,
            participants_limit: int,
            adventure: Adventure,
            password: str | None = None,
            participants_logged: int = 1
    ) -> None:
        await self.session.merge(
            Room(
                participants_logged=participants_logged,
                owner=owner_id,
                name=name,
                participants_limit=participants_limit,
                adventure=adventure,
                password=bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8') if password else None
            )
        )

    async def get_by_name(self, room_name: str):
        return await self.session.scalar(
            select(Room).where(Room.name == room_name).limit(1)
        )

    async def get_all_rooms(self):
        stmt = select(Room)
        return [item for item in await self.session.scalars(stmt)]

    async def new_participant(self, room_id: int):
        stmt = update(Room).where(Room.id == room_id).values(
            participants_logged=Room.participants_logged + 1
        )
        await self.session.execute(stmt)
        await self.session.commit()
