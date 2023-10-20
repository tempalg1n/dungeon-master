"""This file represents a start logic."""

from aiogram import Router, types
from aiogram.filters import CommandStart, Command
from aiogram_dialog import DialogManager, StartMode

from src.bot.structures.FSM.dialog_fsm import BasicSG

basic_router = Router(name='basic')


@basic_router.message(CommandStart())
async def start_handler(message: types.Message, dialog_manager: DialogManager):
    """Start command handler."""
    await dialog_manager.start(BasicSG.greeting, mode=StartMode.RESET_STACK)


@basic_router.message(Command("help"))
async def start_handler(message: types.Message, dialog_manager: DialogManager):
    """Help command handler."""
    await dialog_manager.start(BasicSG.help, mode=StartMode.RESET_STACK)
