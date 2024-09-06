import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
WEBHOOK_HOST = os.getenv('WEBHOOK_HOST')
WEBAPP_HOST = os.getenv('WEBAPP_HOST')
WEBAPP_PORT = int(os.getenv('WEBAPP_PORT'))
CERT_NAME = os.getenv('CERT_NAME')
SCHEDULE_PATH = os.getenv('SCHEDULE_PATH')
FIRST_WEEK_NUMBER = int(os.getenv('FIRST_WEEK_NUMBER'))
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

WEBHOOK_PATH = f'/webhook/{BOT_TOKEN}/'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"
