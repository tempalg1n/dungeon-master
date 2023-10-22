import logging
from typing import Any

import bcrypt
from aiogram import F, Router
from aiogram.enums import ContentType
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import Window, DialogManager, Dialog, ChatEvent
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import SwitchTo, ScrollingGroup, Select, Button, Start, Cancel, Row, Back, Group
from aiogram_dialog.widgets.text import Format, Const

from src.bot.logic.dialogs.translation.i18n_format import I18NFormat
from src.bot.logic.getters.rooms import rooms_getter, number_of_participants_getter, new_room_info_getter, room_getter
from src.bot.structures.FSM.dialog_fsm import RoomsSG, RoomsEditorSG, PlayerCardSG
from src.bot.structures.universe import Adventure
from src.db import Database, Room, Character
from src.db.models import User

logger = logging.getLogger(__name__)


async def select_room(
        c: CallbackQuery,
        widget: Any,
        manager: DialogManager,
        item_id: str,
        *args,
        **kwargs
):
    db: Database = manager.middleware_data.get('db')
    room: Room = await db.room.get_by_name(item_id)
    user: User = await db.user.get_by_tg_id(c.from_user.id)
    character: Character = await db.character.get_by_owner_and_room(owner_id=user.id, room_id=room.id)
    manager.dialog_data['room_name'] = item_id
    if character:
        await c.answer(await I18NFormat('successful-connect').render_text(data={}, manager=manager))
        await manager.switch_to(RoomsSG.room_main)
    else:
        if room.participants_logged < room.participants_limit:
            if room.password:
                await manager.switch_to(RoomsSG.password)
            else:
                character: Character = Character(
                    name=c.from_user.full_name,
                    owner_id=user.id,
                    room=room
                )
                db.session.add(character)
                await db.room.new_participant(room_id=room.id)
                await manager.switch_to(RoomsSG.room_main)
        else:
            await c.answer(await I18NFormat('room-is-full').render_text(data={}, manager=manager))


async def move_without_password(
        c: CallbackQuery,
        widget: Any,
        manager: DialogManager,
        *args,
        **kwargs
):
    await manager.next()


async def change_participants_number(
        callback: ChatEvent,
        select: Any,
        manager: DialogManager,

):
    if select.widget_id == 'increment':
        manager.dialog_data['number_of_participants'] += 1
    elif select.widget_id == 'decrement':
        manager.dialog_data['number_of_participants'] -= 1


async def leave_room(
        callback: ChatEvent,
        select: Any,
        manager: DialogManager,

):
    db: Database = manager.middleware_data.get('db')


async def select_adventure(
        callback: ChatEvent,
        select: Any,
        manager: DialogManager,
        item_id: str,
        *args,
        **kwargs

):
    manager.dialog_data['adventure'] = item_id
    await manager.next()


async def new_room_confirmation(
        callback: ChatEvent,
        select: Any,
        manager: DialogManager,
):
    if select.widget_id == 'confirm':
        db: Database = manager.middleware_data.get('db')
        room_name: str = manager.dialog_data['room_name']
        password: str = manager.dialog_data.get('password', None)
        number_of_participants: int = manager.dialog_data['number_of_participants']
        adventure: Adventure = getattr(Adventure, manager.dialog_data.get("adventure"))
        user: User = await db.user.get_by_tg_id(callback.from_user.id)
        try:
            room: Room = Room(
                owner=user.id,
                name=room_name,
                password=password,
                participants_limit=number_of_participants,
                participants_logged=1,
                adventure=adventure
            )
            character: Character = Character(
                name=callback.from_user.full_name,
                owner_id=user.id,
                room=room
            )
            db.session.add(character)
            await db.session.commit()

            await callback.answer(await I18NFormat('room-creation-success').render_text(manager=manager, data={}))
        except Exception as e:
            logger.critical(e)
            await callback.answer(await I18NFormat('room-creation-error').render_text(manager=manager, data={}))
    else:
        await callback.answer(await I18NFormat('room-creation-cancel').render_text(manager=manager, data={}))

    await manager.start(RoomsSG.rooms)


async def room_name_handler(
        message: Message,
        message_input: MessageInput,
        manager: DialogManager
):
    db: Database = manager.middleware_data.get('db')
    room: Room = await db.room.get_by_name(message.text)
    if not room:
        manager.dialog_data['room_name'] = message.text
        await manager.next()
    else:
        await message.reply(await I18NFormat('room-already-exists').render_text(data={}, manager=manager))
        return


async def password_handler(
        message: Message,
        message_input: MessageInput,
        manager: DialogManager
):
    manager.dialog_data['password'] = message.text
    await manager.next()


async def password_validator_handler(
        message: Message,
        message_input: MessageInput,
        manager: DialogManager
):
    room_name: str = manager.dialog_data.get('room_name')
    db: Database = manager.middleware_data.get('db')
    room: Room = await db.room.get_by_name(room_name)
    pwhash = bcrypt.checkpw(message.text.encode('utf-8'), room.password.encode('utf-8'))
    if pwhash:
        await message.reply(await I18NFormat('successful-connect').render_text(data={}, manager=manager))
        await manager.next()
    else:
        await message.answer(await I18NFormat('wrong-password').render_text(data={}, manager=manager))


async def other_type_handler(
        message: Message,
        message_input: MessageInput,
        manager: DialogManager
):
    await message.answer(await I18NFormat('wrong-name').render_text(manager=manager, data={}))


rooms = Window(
    I18NFormat("rooms", when='rooms'),
    I18NFormat("no-rooms", when=~F['rooms']),
    ScrollingGroup(
        Select(
            text=Format('{item.name} [{item.participants_logged}/{item.participants_limit}]'),
            id='key',
            items='rooms',
            item_id_getter=lambda x: x.name,
            on_click=select_room
        ),
        id='rooms_kb',
        width=1,
        height=5,
        when='rooms'
    ),
    Start(text=I18NFormat('create-new-room'), id='create_room', state=RoomsEditorSG.new_room),
    getter=rooms_getter,
    state=RoomsSG.rooms,
)

password_waiting = Window(
    I18NFormat('enter-password'),
    MessageInput(password_validator_handler, content_types=[ContentType.TEXT]),
    MessageInput(other_type_handler),
    Back(I18NFormat('back')),
    state=RoomsSG.password
)

room_main = Window(
    I18NFormat('room-main'),
    Start(I18NFormat('my-card'), id='my_card', state=PlayerCardSG.main, data=F.get('room_name')),
    Button(I18NFormat('leave-room'), id='leave_room', on_click=leave_room),
    getter=room_getter,
    state=RoomsSG.room_main
)

create_room = Dialog(
    Window(
        I18NFormat('enter-room-name'),
        MessageInput(room_name_handler, content_types=[ContentType.TEXT]),
        MessageInput(other_type_handler),
        Cancel(I18NFormat('cancel')),
        state=RoomsEditorSG.new_room
    ),
    Window(
        I18NFormat('choose-adventure'),
        Group(
            Select(
                Format('{item}'),
                id='adventure',
                item_id_getter=lambda x: x,
                items=Adventure.__dict__['_member_names_'],
                on_click=select_adventure
            ),
            width=2,
        ),
        Back(I18NFormat('back')),
        state=RoomsEditorSG.adventure
    ),
    Window(
        I18NFormat('participants'),
        Const('\n\n'),
        Format("{counter_bar}"),
        Row(
            Button(Const("➖"), id='decrement', on_click=change_participants_number),
            Button(Const("➕"), id='increment', on_click=change_participants_number),
        ),
        SwitchTo(I18NFormat('confirm'), id='confirm_participants', state=RoomsEditorSG.password),
        Back(I18NFormat('back')),
        getter=number_of_participants_getter,
        state=RoomsEditorSG.participants
    ),
    Window(
        I18NFormat('enter-password'),
        MessageInput(password_handler, content_types=[ContentType.TEXT]),
        MessageInput(other_type_handler),
        Button(I18NFormat('without-password'), id='without_password', on_click=move_without_password),
        Back(I18NFormat('back')),
        state=RoomsEditorSG.password
    ),
    Window(
        I18NFormat('confirm-new-room'),
        Row(
            Button(I18NFormat('decline'), id='decline', on_click=new_room_confirmation),
            Button(I18NFormat('confirm'), id='confirm', on_click=new_room_confirmation),
        ),
        Back(I18NFormat('back')),
        getter=new_room_info_getter,
        state=RoomsEditorSG.confirmation
    )
)

rooms_dialog = Dialog(
    rooms,
    password_waiting,
    room_main
)

rooms_router = Router()
rooms_router.include_routers(
    rooms_dialog,
    create_room
)
