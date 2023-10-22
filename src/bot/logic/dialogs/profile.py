import asyncio
from typing import Any

from aiogram import Router
from aiogram_dialog import Window, ChatEvent, DialogManager, Dialog
from aiogram_dialog.widgets.kbd import SwitchTo, Select
from aiogram_dialog.widgets.text import Format

from src.bot.logic.dialogs.translation.i18n_format import I18NFormat
from src.bot.logic.getters.profile import language_code_to_human, profile_getter
from src.bot.structures.FSM.dialog_fsm import ProfileSG
from src.db import Database


async def change_lang(
        callback: ChatEvent,
        select: Any,
        manager: DialogManager,
        item_id: str
):
    db: Database = manager.middleware_data.get('db')
    await db.user.set_lang(item_id, manager.event.from_user.id)
    await callback.answer(await I18NFormat('language-changed').render_text(data={"lang": item_id}, manager=manager))
    await asyncio.sleep(1)
    await manager.switch_to(ProfileSG.profile)


profile = Window(
    I18NFormat("profile"),
    SwitchTo(
        text=I18NFormat('change-lang'),
        id='change_lang',
        state=ProfileSG.language
    ),
    getter=profile_getter,
    state=ProfileSG.profile,
)

language = Window(
    I18NFormat("choose-lang"),
    Select(
        Format("{item}"),
        items=["🇷🇺 Русский", "🇺🇸 English"],
        item_id_getter=language_code_to_human,
        id="w_age",
        on_click=change_lang,
    ),
    state=ProfileSG.language,
)

profile_dialog = Dialog(
    profile,
    language
)

profile_router = Router()
profile_router.include_routers(
    profile_dialog
)
