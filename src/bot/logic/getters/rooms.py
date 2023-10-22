from aiogram_dialog import DialogManager

from src.bot.structures.universe import Adventure
from src.db import Database, Room, Character
from src.db.models import User


async def rooms_getter(
        dialog_manager: DialogManager,
        **kwargs
):
    db: Database = dialog_manager.middleware_data.get('db')
    rooms: list[Room] = await db.room.get_all_rooms()
    rooms_res: dict = {
        'rooms': rooms
    }

    return rooms_res


async def number_of_participants_getter(
        dialog_manager: DialogManager,
        **kwargs
):
    if dialog_manager.dialog_data.get('number_of_participants', 3) <= 3:
        dialog_manager.dialog_data['number_of_participants'] = 3
    elif dialog_manager.dialog_data.get('number_of_participants', 1) >= 10:
        dialog_manager.dialog_data['number_of_participants'] = 10
    number_of_participants: int = dialog_manager.dialog_data['number_of_participants']
    if number_of_participants < 1:
        number_of_participants = 1
    elif number_of_participants > 10:
        number_of_participants = 10

    counter_bar: str = f'<pre>{number_of_participants} ' + '■' * number_of_participants + '□' * (
            10 - number_of_participants) + ' 10</pre>'
    return {
        "number_of_participants": number_of_participants,
        "counter_bar": counter_bar
    }


async def new_room_info_getter(
        dialog_manager: DialogManager,
        **kwargs
):
    room_name: str = dialog_manager.dialog_data.get('room_name')
    adventure: Adventure = getattr(Adventure, dialog_manager.dialog_data.get('adventure'))
    participants: int = dialog_manager.dialog_data.get('number_of_participants')
    return {
        "room_name": room_name,
        "adventure": adventure,
        "number_of_participants": participants
    }


async def room_getter(
        dialog_manager: DialogManager,
        **kwargs
):
    db: Database = dialog_manager.middleware_data.get('db')
    room_name: str = dialog_manager.dialog_data['room_name']
    room: Room = await db.room.get_by_name(room_name)

    participants_logged: int = room.participants_logged
    participants_limit: int = room.participants_limit
    characters: list[Character] = await db.character.get_all_characters_in_room(room_id=room.id)
    users: list[User] = await db.user.get_many_by_ids([character.owner_id for character in characters])
    links: list[str] = []
    for user in users:
        if user.user_name:
            links.append('<a href="tg://resolve?domain={username}">{username}</a>'.format(username=user.user_name))
        else:
            links.append(user.first_name)

    return {
        "room_name": room_name,
        "participants_logged": participants_logged,
        "participants_limit": participants_limit,
        "universe": room.adventure,
        "characters": characters,
        "users": users,
        "players": ", ".join(links),
        "free_places": room.participants_limit - room.participants_logged
    }
