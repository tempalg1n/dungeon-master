"""This package is used for a bot logic implementation."""
from src.bot.logic.dialogs.basic_commands import basic_router_dialogs
from src.bot.logic.dialogs.player_card import card_router
from src.bot.logic.dialogs.profile import profile_router
from src.bot.logic.dialogs.rooms import rooms_router
from src.bot.logic.handlers.basic import basic_router

routers = (
    basic_router,
    basic_router_dialogs,
    profile_router,
    rooms_router,
    card_router
)
