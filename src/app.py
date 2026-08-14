import logging

from aiogram.types import Update
from aiogram.types.input_file import FSInputFile
from aiohttp import web

from telegram_bot.bot_template import BotTemplate


class WebhookApp:
    def __init__(self, bot: BotTemplate, webhook_path: str, webhook_url: str, cert_name: str | None) -> None:
        self.bot: BotTemplate = bot
        self.webhook_url: str = webhook_url
        self.webhook_path: str = webhook_path
        self.cert_name: str | None = cert_name

        self.app = web.Application()
        self.logger = logging.getLogger(__name__)

        self._on_startup()
        self._on_shutdown()
        self._on_update()

    def run(self, host: str | None, port: int) -> None:
        web.run_app(self.app,
                    host=host,
                    port=port)

    def _on_startup(self) -> None:
        async def on_startup(app: web.Application) -> None:
            await self.bot.init()
            self.logger.info(f"Starting webhook on {self.webhook_url}")
            if self.cert_name:
                self.logger.info(f"Using certificate {self.cert_name}")
                await self.bot.set_webhook(self.webhook_url,
                                           certificate=FSInputFile(f"/ssl_keys/{self.cert_name}"))
            else:
                self.logger.info("External certificate used")
                await self.bot.set_webhook(self.webhook_url)

        self.app.on_startup.append(on_startup)

    def _on_shutdown(self) -> None:
        async def on_shutdown(app: web.Application) -> None:
            self.logger.info("Shutting down webhook")
            await self.bot.delete_webhook()

        self.app.on_shutdown.append(on_shutdown)

    def _on_update(self) -> None:
        async def handle(request: web.Request) -> web.Response:
            body = await request.json()
            update = Update(**body)
            if self.bot.dp is None:
                raise RuntimeError("Dispatcher не инициализирован")
            await self.bot.dp.feed_update(self.bot, update)
            return web.Response()

        self.app.router.add_post(self.webhook_path, handle)
