import logging

from colorlog import ColoredFormatter

from app import WebhookApp
from config import (
    ADMINS,
    BOT_TOKEN,
    CERT_NAME,
    DEBUG,
    SCHEDULE_PATH,
    WEBAPP_HOST,
    WEBAPP_PORT,
    WEBHOOK_PATH,
    WEBHOOK_URL,
)
from telegram_bot import TelegramBot


def main():
    formatter = ColoredFormatter(
        '%(black)s%(asctime)s %(log_color)s%(levelname)-8s %(purple)s%(name)s:%(reset)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red',
        }
    )
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logging.basicConfig(level=logging.DEBUG if DEBUG else logging.INFO,
                        handlers=[handler])

    bot = TelegramBot(BOT_TOKEN, SCHEDULE_PATH, ADMINS)

    app = WebhookApp(bot, WEBHOOK_PATH, WEBHOOK_URL, CERT_NAME)
    app.run(WEBAPP_HOST, WEBAPP_PORT)


if __name__ == '__main__':
    main()
