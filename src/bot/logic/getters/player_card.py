from aiogram_dialog import DialogManager


async def player_card_getter(
        dialog_manager: DialogManager,
        **kwargs
):
    room_name: str = dialog_manager.start_data
    profile: dict = {
        'name': dialog_manager.event.from_user.full_name
    }
    return profile
