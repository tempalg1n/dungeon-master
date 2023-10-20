from aiogram import Router
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Row, Button, Cancel

from src.bot.logic.getters.start import get_data
from src.bot.logic.dialogs.translation.i18n_format import I18NFormat
from src.bot.structures.FSM.dialog_fsm import BasicSG

commands = Dialog(
    Window(
        I18NFormat("Hello-user"),
        getter=get_data,
        state=BasicSG.greeting,
    ),
    Window(
        I18NFormat("help"),
        state=BasicSG.help
    )
)

basic_router_dialogs = Router()
basic_router_dialogs.include_routers(
    commands
)
