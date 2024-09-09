import logging

from aiogram import BaseMiddleware


class AdminCommandMiddleware(BaseMiddleware):
    def __init__(self, allowed_users, admin_commands):
        super().__init__()

        self.logger = logging.getLogger(__name__)

        self.allowed_users = allowed_users
        self.admin_commands = admin_commands

    async def __call__(self, handler, event, data):
        self.logger.debug(f"Event: {event}")
        self.logger.debug(f"Data: {data}")
        if event.message.text and event.message.text.startswith('/'):
            command = event.message.text.split()[0].split('@')[0][1:]
            self.logger.debug(f"Command: {command}")
            self.logger.debug(f"{command} in {self.admin_commands}")
            self.logger.debug(f"{event.message.from_user.id} in {self.allowed_users}")
            if command in self.admin_commands and event.message.from_user.id not in self.allowed_users:
                return
        return await handler(event, data)

