from any_link import ensure_list, download_image
import requests
import argparse


def get_links_spacex(spacex_id=None):
    """Получает список ссылок с SpaceX-API.

    Возвращает список ссылок на оригинальные фотографии запуска
    если их нет то возвращает пустой список.

    Args:
        spacex_id (str): ID запуска, например: 5eb87d47ffd86e000604b38a.

    Returns:
        list: Список строк с URL изображений.
    """
    if not spacex_id:
        spacex_id = 'latest'
    url = f"https://api.spacexdata.com/v5/launches/{spacex_id}"

    response = requests.get(url)
    response.raise_for_status()

    some_links = response.json().get('links', {}).get(
        'flickr', {}).get('original', [])

    return some_links


def create_parser():
    parser = argparse.ArgumentParser(
        description='Запускает работу с SpaceX-API и сохраняет фото'
    )
    parser.add_argument('spacex_id',
                        nargs='?',
                        default='latest',
                        help='ID запуска (по умолчанию последний)'
                        )
    return parser


def main():
    """Запускает работу с API и сохраняет фото."""
    parser = create_parser()
    args = parser.parse_args()

    name_photo = input("Введите название фото: ").strip().lower()
    path = input("Введите путь или Enter: ").strip() or 'images/'
    try:
        some_links = get_links_spacex(args.spacex_id)
        links_photo = ensure_list(some_links)
    except requests.exceptions.ReadTimeout:
        print("Превышено время ожидания...")
        return

    except requests.exceptions.ConnectionError as error:
        print(error, "Ошибка соединения")
        return

    except Exception as error:
        print(error, "ERROR_2")
        return

    if not links_photo:
        print("Фотографии не найдены.")
        return
    for number_links, link in enumerate(links_photo, start=1):
        number_photo = number_links if len(links_photo) > 1 else None
        saved_path = download_image(link, name_photo, path, number_photo)
        print(f"Файл сохранён: {saved_path}")


if __name__ == '__main__':
    main()
