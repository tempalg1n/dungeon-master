from typing import Any

from aiogram import Router
from aiogram_dialog import Window, Dialog, ChatEvent, DialogManager
from aiogram_dialog.widgets.kbd import ScrollingGroup, Select, Start
from aiogram_dialog.widgets.text import Format

from src.bot.logic.dialogs.translation.i18n_format import I18NFormat
from src.bot.logic.getters.player_card import player_card_getter
from src.bot.structures.FSM.dialog_fsm import PlayerCardSG


async def select_field(
        callback: ChatEvent,
        select: Any,
        manager: DialogManager,
        item_id: str,
        *args,
        **kwargs

):
    manager.dialog_data['field'] = item_id


plater_card_main = Window(
    I18NFormat("card-main"),
    ScrollingGroup(
        Select(
            text=Format('{item.name} [{item.participants_logged}/{item.participants_limit}]'),
            id='card_field',
            items='fields',
            item_id_getter=lambda x: x.name,
            on_click=select_field
        ),
        id='rooms_kb',
        width=1,
        height=5,
        when='rooms'
    ),
    getter=player_card_getter,
    state=PlayerCardSG.main,
)

card_dialog = Dialog(
    plater_card_main
)

card_router = Router()
card_router.include_routers(
    card_dialog,
)
