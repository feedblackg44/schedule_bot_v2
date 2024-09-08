import logging

from aiogram.types import Message

from enums import WeekType
from schedule import Maker
from .admin_command_middleware import AdminCommandMiddleware
from .bot_template import BotTemplate


class TelegramBot(BotTemplate):
    def __init__(self, token, path, admins=None):

        self.logger = logging.getLogger(__name__)

        self.schedule_maker = Maker(path)
        self.admins = admins

        self.schedule = None
        self.teachers = None
        self.disciplines = None

        link, group = self.make_schedule()

        super().__init__(token=token, schedule_link=link, group=group)

        admin_middleware = AdminCommandMiddleware(self.admins, self.admin_commands)
        self.dp.update.middleware(admin_middleware)

        self.make_commands()

    def make_schedule(self):
        self.schedule, self.teachers, self.disciplines = self.schedule_maker.make()

        return self.schedule.link, self.schedule.group

    def make_commands(self):
        self.start_command()
        self.help_command()
        self.full_command()
        self.week_command()
        self.nextweek_command()
        self.today_command()
        self.tomorrow_command()
        self.left_command()

        self.teachers_command()
        self.timetable_command()
        self.extra_command()

        self.make_discipline_commands()

        self.reload_schedule_command()

    def reload_schedule_command(self):
        self.logger.info("Создание команды /reload")
        @self.admin_command("reload")
        async def reload_schedule(message: Message):
            self.reset_commands()
            self.make_schedule()
            self.make_commands()
            await self.init()
            await self.send_safe_message(message, "Розклад перезавантажено")

    def start_command(self):
        self.logger.info("Создание команды /start")
        @self.command("start", "Привітання")
        async def send_welcome(message: Message):
            await self.send_safe_message(message, self.make_help_command())

    def help_command(self):
        self.logger.info("Создание команды /help")
        @self.command("help", "Допомога")
        async def send_help(message: Message):
            await self.send_safe_message(message, self.make_help_command())

    def left_command(self):
        self.logger.info("Создание команды /left")
        @self.command("left", "Час до наступної пари/до кінця поточної")
        async def send_left_time(message: Message):
            await self.send_safe_message(message, self.schedule.left())

    def today_command(self):
        self.logger.info("Создание команды /today")
        @self.command("today", "Розклад на сьогодні")
        async def send_today_schedule(message: Message):
            answer = self.schedule.today()
            if not isinstance(answer, str):
                answer = answer.to_str(use_time=True)
            await self.send_safe_message(message, answer)

    def tomorrow_command(self):
        self.logger.info("Создание команды /tomorrow")
        @self.command("tomorrow", "Розклад на завтра")
        async def send_tomorrow_schedule(message: Message):
            answer = self.schedule.tomorrow()
            if not isinstance(answer, str):
                answer = answer.to_str(use_time=True)
            await self.send_safe_message(message, answer)

    def week_command(self):
        self.logger.info("Создание команды /week")
        @self.command("week", "Розклад на тиждень")
        async def send_week_schedule(message: Message):
            await self.send_safe_message(message, self.schedule.to_str(week=WeekType.CURRENT))

    def nextweek_command(self):
        self.logger.info("Создание команды /nextweek")
        @self.command("nextweek", "Розклад на наступний тиждень")
        async def send_next_week_schedule(message: Message):
            await self.send_safe_message(message, self.schedule.to_str(week=WeekType.NEXT))

    def full_command(self):
        self.logger.info("Создание команды /full")
        @self.command("full", "Повний розклад")
        async def send_full_schedule(message: Message):
            await self.send_safe_message(message, str(self.schedule))

    def teachers_command(self):
        self.logger.info("Создание команды /teachers")
        @self.command("teachers", "Викладачі")
        async def send_teachers(message: Message):
            str_out = "🎓 Викладачі 🎓\n\n"
            for idx, teacher in enumerate(self.teachers.values()):
                str_out += f"- {teacher}"
                if idx != len(self.teachers):
                    str_out += "\n"
            await self.send_safe_message(message, str_out)

    def timetable_command(self):
        self.logger.info("Создание команды /timetable")
        @self.command("timetable", "Розклад занять")
        async def send_timetable(message: Message):
            str_out = "🗓 Розклад дзвінків 🗓\n\n"
            for idx, lesson_time in enumerate(self.schedule.timetable, start=1):
                str_out += (f"{idx} пара:  {lesson_time['start'].strftime('%H:%M')} - "
                            f"{lesson_time['end'].strftime('%H:%M')}")
                if idx - 1 != len(self.schedule.timetable):
                    str_out += "\n"
            await self.send_safe_message(message, str_out)

    def make_discipline_commands(self):
        for name, discipline in self.disciplines.items():
            self.logger.info(f"Создание команды /{discipline.command}")
            @self.command(discipline.command, f"{name}", discipline=True)
            async def send_discipline_schedule(message: Message, disc=discipline):
                await self.send_safe_message(message, str(disc))

    def extra_command(self):
        if self.schedule.extra:
            self.logger.info("Создание команды /extra")
            @self.command("extra", "Додаткова інформація")
            async def send_extra(message: Message):
                await self.send_safe_message(message, self.schedule.str_extra())
        else:
            self.logger.info("Додаткова інформація відсутня")
