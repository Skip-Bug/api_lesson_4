from utils import ensure_list, download_image, add_common_args
import requests
import argparse


def create_parser():
    """Добавляет аргументы для скрипта."""
    parser = argparse.ArgumentParser(
        description='Запускает работу с SpaceX-API и сохраняет фото'
    )
    parser.add_argument(
        'spacex_id',
        nargs='?',
        default='latest',
        help='ID запуска (по умолчанию последний)'
    )
    add_common_args(parser)
    return parser


def get_links_spacex(spacex_id):
    """Получает список ссылок с SpaceX-API.

    Возвращает список ссылок на оригинальные фотографии запуска
    если их нет то возвращает пустой список.

    Args:
        spacex_id (str): ID запуска, например: 5eb87d47ffd86e000604b38a.

    Returns:
        list: Список строк с URL изображений.
    """
    url = f"https://api.spacexdata.com/v5/launches/{spacex_id}"

    response = requests.get(url)
    response.raise_for_status()

    some_links = response.json().get('links', {}).get(
        'flickr', {}).get('original', [])

    return some_links


def main():
    """Запускает работу с API и сохраняет фото."""
    parser = create_parser()
    args = parser.parse_args()

    name_photo = args.name.strip().lower() if args.name else None
    path = args.path.strip() if args.path else 'images/'

    some_links = None
    try:
        some_links = get_links_spacex(args.spacex_id)

    except requests.exceptions.RequestException as error:
        print(f"Ошибка запроса к SpaceX API: {error}")
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
