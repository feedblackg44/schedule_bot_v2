import logging

from aiogram.types.input_file import FSInputFile
from aiogram.types import Update
from aiohttp import web


class WebhookApp:
    def __init__(self, bot, webhook_path, webhook_url, cert_name):
        self.bot = bot
        self.dp = bot.dp
        self.webhook_url = webhook_url
        self.webhook_path = webhook_path
        self.cert_name = cert_name

        self.app = web.Application()
        self.logger = logging.getLogger(__name__)

        self._on_startup()
        self._on_shutdown()
        self._on_update()


    def run(self, host, port):
        web.run_app(self.app,
                    host=host,
                    port=port)

    def _on_startup(self):
        async def on_startup(app):
            await self.bot.init()
            self.logger.info(f"Starting webhook on {self.webhook_url}")
            if self.cert_name:
                await self.bot.set_webhook(self.webhook_url,
                                           certificate=FSInputFile(f"/ssl_keys/{self.cert_name}"))
            else:
                await self.bot.set_webhook(self.webhook_url)

        self.app.on_startup.append(on_startup)

    def _on_shutdown(self):
        async def on_shutdown(app):
            self.logger.info("Shutting down webhook")
            await self.bot.delete_webhook()

        self.app.on_shutdown.append(on_shutdown)

    def _on_update(self):
        async def handle(request):
            body = await request.json()
            update = Update(**body)
            await self.dp.feed_update(self.bot, update)
            return web.Response()

        self.app.router.add_post(self.webhook_path, handle)