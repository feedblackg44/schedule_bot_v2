# Telegram Schedule Bot

This Telegram bot helps users keep track of online lessons and conveniently store information such as links or start times, ensuring that no lesson is missed. Built with `aiogram` 3.12 and Python 3.11, it offers an easy-to-use interface for managing all your lesson details.

## Features
- **Flexible Scheduling**: Easily configure lesson schedules using a YAML configuration file.
- **Secure Webhooks**: Supports secure communication via webhooks with SSL.
- **Timezone Support**: Automatically adjusts schedules based on the specified timezone.
- **Customizable Configuration**: Configure bot settings through `.env` and `config.yaml` files.

## Requirements

- Docker and Docker Compose installed.

## Installation

1. Clone the repository:
```bash
git clone git@github.com:feedblackg44/schedule_bot_v2.git
cd schedule_bot_v2
```
2. Create a `.env` file in the `Docker/` directory of the project with the following structure:
```env
BOT_TOKEN=bot_token
WEBHOOK_HOST=https://webhook.host:port
WEBAPP_HOST=0.0.0.0
WEBAPP_PORT=webhook_app_local_port
SSL_CERT=path_to_ssl_certs_folder
CERT_NAME=cert_name or None (if using an external certificate, e.g., from Cloudflare)
SCHEDULE_PATH=path_to_config
FIRST_WEEK_NUMBER=1 or 0 (depending on whether the first week is considered even)
TIMEZONE=Europe/Kiev
```
3. Use the example configuration provided in `config.example.yaml` to set up your initial schedule. 
Create new `config.yaml` based on the example, customizing the schedule to your needs.

## Running the Bot

To run the bot, navigate to the `Docker/` folder and use the following command:

```bash
docker compose up
```
