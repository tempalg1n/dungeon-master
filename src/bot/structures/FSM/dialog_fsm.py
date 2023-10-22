from aiogram.fsm.state import StatesGroup, State


class BasicSG(StatesGroup):
    greeting = State()
    help = State()


class ProfileSG(StatesGroup):
    profile = State()
    language = State()


class RoomsSG(StatesGroup):
    rooms = State()
    room_info = State()
    password = State()
    room_main = State()


class RoomsEditorSG(StatesGroup):
    new_room = State()
    password = State()
    confirmation = State()
    participants = State()
    adventure = State()


class PlayerCardSG(StatesGroup):
    main = State()
