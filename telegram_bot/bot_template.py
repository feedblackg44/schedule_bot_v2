import logging

from aiogram import Bot, Router, Dispatcher
from aiogram.filters import Command
from aiogram.types import BotCommand


class BotTemplate(Bot):
    def __init__(self, token, schedule_link, group):
        super().__init__(token=token)

        self.schedule_link = schedule_link
        self.group = group
        self.logger = logging.getLogger(__name__)

        self.commands = {}
        self.disc_commands = {}
        self.admin_commands = []

        self.dp = None
        self.router = None

        self.reset_commands()

    def reset_commands(self):
        self.dp = Dispatcher()
        self.router = Router()
        self.dp.include_router(self.router)
        self.commands.clear()
        self.disc_commands.clear()

    def make_help_command(self):
        help_message = f'👹 <b>Бот групи <a href="{self.schedule_link}">{self.group}</a></b>👹 \n' + "-" * 50
        help_message += "\nКоманди бота:"
        for command in self.commands:
            help_message += f"\n/{command.command} - {command.description}"
        help_message += "\n" + "-" * 50
        help_message += "\nДисципліни:"
        for command in self.disc_commands:
            help_message += f"\n/{command.command} - {command.description}"

        return help_message

    async def init(self):
        await self.set_user_commands()

    async def set_user_commands(self):
        await self.set_my_commands([*self.commands.values(), *self.disc_commands.values()])

    def command(self, command_name, description, discipline=False):
        def decorator(func):
            self.router.message(Command(command_name))(func)
            if command_name != 'start':
                if not discipline:
                    self.commands[command_name] = BotCommand(command=command_name, description=description)
                else:
                    self.disc_commands[command_name] = BotCommand(command=command_name, description=description)
            return func
        return decorator

    def admin_command(self, command_name):
        def decorator(func):
            self.router.message(Command(command_name))(func)
            if command_name not in self.admin_commands:
                self.admin_commands.append(command_name)
            return func
        return decorator

    async def send_safe_message(self, inc_message, out_message,
                                answer=False,
                                parse_mode="HTML",
                                max_len=4096,
                                disable_web_page_preview=True):
        if not out_message:
            self.logger.warning("Пустое сообщение")
            return
        if len(out_message) > max_len:
            self.logger.warning(f"Сообщение слишком длинное: {len(out_message)}")
            out_messages = out_message.rsplit("\n\n", 1)
            for out_message in out_messages:
                if out_message:
                    await self.send_safe_message(inc_message=inc_message,
                                                 out_message=out_message,
                                                 answer=answer,
                                                 parse_mode=parse_mode,
                                                 max_len=max_len,
                                                 disable_web_page_preview=disable_web_page_preview)
        else:
            if answer:
                await inc_message.answer(out_message,
                                         parse_mode=parse_mode,
                                         disable_web_page_preview=disable_web_page_preview)
            else:
                await self.send_message(inc_message.chat.id, out_message,
                                        parse_mode=parse_mode,
                                        disable_web_page_preview=disable_web_page_preview)
