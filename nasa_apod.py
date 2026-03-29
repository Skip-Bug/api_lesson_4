from utils import ensure_list, download_image, add_common_args
from dotenv import load_dotenv
from datetime import datetime
import argparse
import requests
import os


def create_parser():
    parser = argparse.ArgumentParser(
        description='Запускает работу с NASA APOD API и сохраняет фото'
    )
    parser.add_argument(
        'api_key',
        nargs='?',
        default='DEMO_KEY',
        help='ID NASA APOD API (по умолчанию DEMO_KEY)'
    )
    parser.add_argument(
        '-c',
        '--count', default=None,
        help='Введите количество (1-100)'
    )
    parser.add_argument(
        '-d',
        '--date', default=None,
        help='Введите дату (YYYY-MM-DD)'
    )
    add_common_args(parser)
    return parser


def get_links_nasa_apod(api_key, count=None, date=None):
    """Получает список ссылок на изображения с NASA APOD API.

    Args:
        api_key (str, optional): API-ключ NASA. По умолчанию "DEMO_KEY".
        count (int, optional): Количество случайных изображений (1–100).
            Если указан, возвращает список случайных фото.
        date (str, optional): Дата в формате YYYY-MM-DD.
            Нельзя использовать вместе с count.

    Returns:
        list: Список строк с URL изображений.
            Может быть пустым, если ссылки не найдены.
    """
    params = {'api_key': api_key}
    if count is not None:
        params['count'] = count
    if date is not None:
        params['date'] = date

    base_url = "https://api.nasa.gov/planetary/apod"

    response = requests.get(base_url, params=params)
    response.raise_for_status()

    apod_response = response.json()

    if isinstance(apod_response, dict):
        apod_links = [apod_response]
    else:
        apod_links = apod_response

    some_links = []
    for apod_link in apod_links:
        if apod_link.get('media_type') != 'image':
            continue

        some_link = apod_link.get('url')
        if some_link:
            some_links.append(some_link)
    return some_links


def main():
    """Запускает работу с API и сохраняет фото."""

    load_dotenv()
    parser = create_parser()
    args = parser.parse_args()

    count_input = args.count.strip() if args.count else None
    if count_input:
        try:
            count = int(count_input)
            if not (1 <= count <= 100):
                print("Количество должно быть от 1 до 100.")
                return
            date = None
        except ValueError:
            print(f"'{count_input}' — не число.")
            return
    else:
        count = None
        date_input = args.date.strip() if args.date else None
        if date_input:
            try:
                date = datetime.strptime(
                    date_input, "%Y-%m-%d").strftime("%Y-%m-%d")
            except ValueError:
                print("Неверный формат даты. Нужно YYYY-MM-DD.")
                return
        else:
            date = None

    api_key = args.api_key or os.getenv('NASA_ID')

    name_photo = args.name.strip().lower() if args.name else None
    path = args.path.strip() if args.path else 'images/'

    some_links = None
    try:
        some_links = get_links_nasa_apod(api_key, count, date)

    except requests.exceptions.RequestException as error:
        print(f"Ошибка запроса к NASA APOD API: {error}")
        return

    links_photo = ensure_list(some_links)
    if not links_photo:
        print("Фотографии не найдены.")
        return

    for number_links, link in enumerate(links_photo, start=1):
        number_photo = number_links if len(links_photo) > 1 else None
        try:
            saved_path = download_image(link, name_photo, path, number_photo)
            print(f"Файл сохранён: {saved_path}")
        except requests.exceptions.ReadTimeout:
            print("Превышено время ожидания...")
        except requests.exceptions.ConnectionError as error:
            print(error, "Ошибка соединения")
        except requests.exceptions.HTTPError as error:
            print(f"Ошибка HTTP: {error.response.status_code}")


if __name__ == '__main__':
    main()
