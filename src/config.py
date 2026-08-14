import os

from dotenv import load_dotenv

_ = load_dotenv()


def _require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Переменная окружения {name} обязательна")
    return value


BOT_TOKEN = _require_env('BOT_TOKEN')
WEBHOOK_HOST = os.getenv('WEBHOOK_HOST')
WEBAPP_HOST = os.getenv('WEBAPP_HOST')
WEBAPP_PORT = int(os.getenv('WEBAPP_PORT', '8000'))
cert_name = os.getenv('CERT_NAME')
CERT_NAME = cert_name if cert_name != 'None' else None
SCHEDULE_PATH = _require_env('SCHEDULE_PATH')
FIRST_WEEK_NUMBER = int(os.getenv('FIRST_WEEK_NUMBER', '0'))
ADMINS = {int(admin_id) for admin_id in os.getenv('ADMINS', '').split(',') if admin_id.strip()}
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

WEBHOOK_PATH = f'/webhook/{BOT_TOKEN}/'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"
