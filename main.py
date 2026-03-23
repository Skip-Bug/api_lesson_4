from telegram import Bot
from telegram.utils.request import Request
from dotenv import load_dotenv
import argparse
import random
import time
import os


def time_parser():
    """Дает возможность выбирать задержку публикаций."""
    parser = argparse.ArgumentParser(
        description='Запускает работу бота с задержкой'
    )
    parser.add_argument('sleep',
                        nargs='?',
                        default='14400',
                        help='Задержка публикаций (по умолчанию 4 часа)'
                        )
    parser.add_argument('-p', '--photo', help='Выбрать фото для старта')
    return parser


def main():
    """ Запускает Бота который опубликует изображения.

    Если указан аргумент -p/--photo, сначала отправляет это фото,
    затем переходит к бесконечному циклу отправки всех фото из папки images.
    Не оставляйте папку images пусто больше чем на 1 час.
    Иначе сразу работает в бесконечном цикле.
    Задержка между отправками задаётся первым аргументом (в секундах, по умолчанию 14400).
    Ctrl+C останавливает бота.
    """
    load_dotenv()
    images_folder = "images"
    channel_id = os.getenv("TG_CHANNEL_ID")
    token = os.getenv('TG_BOT_TOKEN')
    proxy_url = os.getenv('PROXY_URL') or None

    if not channel_id:
        print("Канал не обнаружен")
        return
    if not token:
        print(" Токен не найден в .env")
        return

    parser = time_parser()
    args = parser.parse_args()
    try:
        sleep_seconds = int(args.sleep)
    except ValueError:
        print("Ошибка: задержка задается в секундах")
        return
    request = Request(proxy_url=proxy_url, connect_timeout=20, read_timeout=20)
    bot = Bot(token=token, request=request)
    if args.photo:
        image_path = os.path.join(images_folder, args.photo)
        if not os.path.exists(image_path):
            print(f"Файл {image_path} не найден")
            return
        with open(image_path, 'rb') as photo:
            bot.send_photo(chat_id=channel_id, photo=photo,
                           caption="Привет от Бота!")
    try:
        while True:
            images = os.listdir(images_folder)
            if not images:
                print("Папка пуста")
                time.sleep(3600)
                continue
            random.shuffle(images)
            for image_file in images:
                image_path = os.path.join(images_folder, image_file)
                with open(image_path, 'rb') as image:
                    bot.send_photo(chat_id=channel_id, photo=image,
                                   caption="Привет от Бота!")
                time.sleep(sleep_seconds)

    except KeyboardInterrupt:
        print("\nБот остановлен пользователем.")
        bot.send_message(chat_id=channel_id, text="Бот завершил работу")

    except Exception as exp:
        print(f"Ошибка: {exp}")
        bot.send_message(chat_id=channel_id, text="Я сломался")


if __name__ == '__main__':
    main()
