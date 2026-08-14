import logging
from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Update


class AdminCommandMiddleware(BaseMiddleware):
    def __init__(self, allowed_users: set[int] | None, admin_commands: list[str]) -> None:
        super().__init__()

        self.logger = logging.getLogger(__name__)

        self.allowed_users: set[int] | None = allowed_users
        self.admin_commands: list[str] = admin_commands

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        self.logger.debug(f"Event: {event}")
        self.logger.debug(f"Data: {data}")
        if (
            isinstance(event, Update)
            and event.message
            and event.message.text
            and event.message.text.startswith('/')
            and event.message.from_user
        ):
            command = event.message.text.split()[0].split('@')[0][1:]
            self.logger.debug(f"Command: {command}")
            self.logger.debug(f"{command} in {self.admin_commands}")
            self.logger.debug(f"{event.message.from_user.id} in {self.allowed_users}")
            if command in self.admin_commands and event.message.from_user.id not in (self.allowed_users or set()):
                return
        return await handler(event, data)
