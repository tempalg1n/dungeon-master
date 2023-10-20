"""This package is used for a bot logic implementation."""
from src.bot.logic.dialogs.basic_commands import basic_router_dialogs
from src.bot.logic.handlers.basic import basic_router

routers = (
    basic_router,
    basic_router_dialogs
)
