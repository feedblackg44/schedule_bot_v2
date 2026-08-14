import logging
from datetime import datetime

from aiogram import Bot, Dispatcher, Router
from aiogram.filters import Command
from aiogram.types import BotCommand, InlineQueryResultArticle, InputTextMessageContent


class BotTemplate(Bot):
    def __init__(self, token, schedule_link, group):
        super().__init__(token=token)

        self.schedule_link = schedule_link
        self.group = group
        self.logger = logging.getLogger(__name__)

        self.commands = {}
        self.disc_commands = {}
        self.admin_commands = []

        self.inline_results = {}

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
        help_message = f'👹 <b>Бот групи <a href="{self.schedule_link}">{self.group}</a></b> 👹\n' + "-" * 50
        help_message += "\nКоманди бота:"
        for command in self.commands.values():
            help_message += f"\n/{command.command} - {command.description}"
        help_message += "\n" + "-" * 50
        help_message += "\nДисципліни:"
        for command in self.disc_commands.values():
            help_message += f"\n/{command.command} - {command.description}"

        return help_message

    async def init(self):
        await self.set_user_commands()

    async def set_user_commands(self):
        await self.set_my_commands([*self.commands.values(), *self.disc_commands.values()])

    def register_inline_result(self):
        if not self.router:
            self.logger.error("Router не инициализирован. Вызовите reset_commands() перед регистрацией inline результатов.")
            return

        @self.router.inline_query()
        async def inline_suggestions(query):
            str_query = query.query.strip().lower()

            self.logger.debug(f"Inline query: '{str_query}', results available: {list(self.inline_results.keys())}")

            current_date = datetime.now().strftime('%Y%m%d_%H')  # noqa: DTZ005 -- naive local time, container TZ set via docker-compose
            suggestions = []
            for command, c_dict in self.inline_results.items():
                if str_query == "" or str_query in command:
                    try:
                        message_text = c_dict['input_message_content']['message_func']()
                        suggestions.append(InlineQueryResultArticle(
                            id=f"{c_dict['id']}_{current_date}",
                            title=c_dict['title'],
                            input_message_content=InputTextMessageContent(
                                message_text=message_text,
                                parse_mode=c_dict['input_message_content']['parse_mode'],
                                disable_web_page_preview=c_dict['input_message_content']['disable_web_page_preview']
                            ),
                            description=c_dict['description']
                        ))
                    except Exception as e:  # noqa: BLE001 -- one bad command's generator must not break the whole inline query
                        self.logger.error(f"Ошибка при формировании inline результата для '{command}': {e}")

            self.logger.debug(f"Returning {len(suggestions)} suggestions")
            await query.answer(suggestions, cache_time=0)

    def command(self, command_name, description,
                discipline=False,
                answer=False,
                parse_mode="HTML",
                disable_web_page_preview=True):
        def decorator(func):
            if not self.router:
                self.logger.error("Router не инициализирован. Вызовите init() перед регистрацией команд.")
                return func
            
            async def func_wrapper(message):
                await self.send_safe_message(message, func(), answer=answer)
            self.router.message(Command(command_name))(func_wrapper)

            self.inline_results[command_name] = {
                'id': command_name,
                'title': command_name,
                'input_message_content': {'message_func': func,
                                          'parse_mode': parse_mode,
                                          'disable_web_page_preview': disable_web_page_preview},
                'description': description
            }

            if command_name != 'start':
                if not discipline:
                    self.commands[command_name] = BotCommand(command=command_name, description=description)
                else:
                    self.disc_commands[command_name] = BotCommand(command=command_name, description=description)
            return func
        return decorator

    def admin_command(self, command_name):
        def decorator(func):
            if not self.router:
                self.logger.error("Router не инициализирован. Вызовите init() перед регистрацией команд.")
                return func
            
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
            for msg in out_messages:
                if msg:
                    await self.send_safe_message(inc_message=inc_message,
                                                 out_message=msg,
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
