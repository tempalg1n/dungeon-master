"""Character repository file."""
import bcrypt
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from .abstract import Repository

from ..models import Character, Base


class CharacterRepo(Repository[Character]):
    """User repository for CRUD and other SQL queries."""

    def __init__(self, session: AsyncSession):
        """Initialize user repository as for all users or only for one user."""
        super().__init__(type_model=Character, session=session)

    async def new(
            self,
            name: str,
            owner_id: int,
            room: type[Base] = None,
    ) -> None:
        await self.session.merge(
            Character(
                name=name,
                owner_id=owner_id,
                room=room
            )
        )

    async def get_by_name(self, room_name: str):
        return await self.session.scalar(
            select(Character).where(Character.name == room_name).limit(1)
        )

    async def get_by_owner_and_room(self, room_id: int, owner_id: int):
        return await self.session.scalar(
            select(Character).where(Character.room_fk == room_id, Character.owner_id == owner_id).limit(1)
        )

    async def get_all_characters_in_room(self, room_id: int):
        stmt = select(Character).where(Character.room_fk == room_id)
        return [item for item in await self.session.scalars(stmt)]
