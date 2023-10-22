from aiogram_dialog import DialogManager


def language_code_to_human(code: str):
    translation: dict[str, str] = {
        '🇷🇺 Русский': 'ru',
        '🇺🇸 English': 'us'
    }
    return translation.get(code, code)


async def profile_getter(
        dialog_manager: DialogManager,
        **kwargs
):
    profile: dict = {
        'name': dialog_manager.event.from_user.full_name
    }
    return profile
