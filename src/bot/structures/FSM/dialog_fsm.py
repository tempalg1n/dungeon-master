from aiogram.fsm.state import StatesGroup, State


class BasicSG(StatesGroup):
    greeting = State()
    help = State()
