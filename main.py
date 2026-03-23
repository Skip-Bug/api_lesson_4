from telegram import Bot
from telegram.utils.request import Request
from dotenv import load_dotenv
import os


def main():
    load_dotenv()
    token = os.getenv('TG_BOT_TOKEN')
    proxy_url = os.getenv('PROXY_URL')
    if not token:
        print(" Токен не найден в .env")
        return

    request = Request(proxy_url=proxy_url, connect_timeout=20, read_timeout=20)
    bot = Bot(token=token, request=request)

    channel_id = "@load_image"  # "-1003711383466"

    bot.send_message(chat_id=channel_id, text="Привет от бота!")


if __name__ == '__main__':
    main()
