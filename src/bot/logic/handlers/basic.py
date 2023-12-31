"""This file represents a start logic."""

from aiogram import Router, types
from aiogram.filters import CommandStart, Command
from aiogram_dialog import DialogManager, StartMode

from src.bot.structures.FSM.dialog_fsm import BasicSG, ProfileSG, RoomsSG

basic_router = Router(name='basic')


@basic_router.message(CommandStart())
async def start_handler(message: types.Message, dialog_manager: DialogManager):
    """Start command handler."""
    await dialog_manager.start(BasicSG.greeting, mode=StartMode.RESET_STACK)


@basic_router.message(Command("help"))
async def help_command_handler(message: types.Message, dialog_manager: DialogManager):
    """Help command handler."""
    await dialog_manager.start(BasicSG.help, mode=StartMode.RESET_STACK)


@basic_router.message(Command("profile"))
async def profile_command_handler(message: types.Message, dialog_manager: DialogManager):
    await dialog_manager.start(ProfileSG.profile, mode=StartMode.RESET_STACK)


@basic_router.message(Command("rooms"))
async def rooms_command_handler(message: types.Message, dialog_manager: DialogManager):
    await dialog_manager.start(RoomsSG.rooms, mode=StartMode.RESET_STACK)
