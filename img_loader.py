from utils import download_image
from utils import add_common_args
import requests
import argparse


def create_parser():
    parser = argparse.ArgumentParser(
        description='Скачивание изображения по ссылке.')
    parser.add_argument('url', help='Ссылка на изображение')
    add_common_args(parser)
    return parser


def main():
    """Запускает обработку ссылок и сохраняет фото."""
    parser = create_parser()
    args = parser.parse_args()

    if not args.url.startswith(('http://', 'https://')):
        print(f"Ссылка '{args.url}' должна начинаться с http:// или https://")
        return

    name_photo = args.name.strip().lower() if args.name else None
    path = args.path.strip() if args.path else 'images/'

    try:
        saved_path = download_image(args.url, name_photo, path)
        print(f"Файл сохранён: {saved_path}")
    except requests.exceptions.ReadTimeout:
        print("Превышено время ожидания...")

    except requests.exceptions.ConnectionError as error:
        print(error, "Ошибка соединения")

    except requests.exceptions.HTTPError as error:
        print(f"Ошибка HTTP: {error.response.status_code}")


if __name__ == '__main__':
    main()
