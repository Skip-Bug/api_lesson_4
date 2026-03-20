from dotenv import load_dotenv
from pathlib import Path
import requests
import os


def getting_extension(links_photo)


"""Функция для получения расширения картинки"""

return


def get_links_nasa(api_key=None):
    """Получает список ссылок с NASA-API .

    Возвращает список ссылок на изображение дня
    если их нет то возвращает пустой список.
    Args:
        api_key: ID для работы с API
        например: DEMO_KEY.
    """
    if api_key is None:
        api_key = "DEMO_KEY"

    url = f"https://api.nasa.gov/planetary/apod?api_key={api_key}"
    response = requests.get(url)
    response.raise_for_status()

    some_links = response.json()
    return some_links.get('hdurl') or some_links.get('url')


def get_links_spacex(id):
    """Получает список ссылок с SpaceX-API .

    Возвращает список ссылок на оригинальные фотографии запуска
    если их нет то возвращает пустой список.
    Args:
        id: ID запуска например: 5eb87d47ffd86e000604b38a.
    """
    url = f"https://api.spacexdata.com/v5/launches/{id}"
    response = requests.get(url)
    response.raise_for_status()

    some_links = response.json().get('links', {}).get(
        'flickr', {}).get('original', [])

    return some_links


def ensure_list(some_links):
    """Приводит значение к списку для универсальной итерации."""
    if isinstance(some_links, list):
        return some_links
    if some_links:
        return [some_links]
    return []


def download_image(url, name_photo, path, number_photo=None,  headers=None):
    """Сохраняет картинку по URL в указанную папку.

    Возвращает путь к сохранённому файлу.

    Args:
        url: Адрес картинки в интернете.
        name_photo: Название фото.
        path: Папка для сохранения (будет создана, если нет).
        number_photo: Номер фото для сохранения
            (если фото одно то сохранится по названию если,
             их несколько то название_1 и т.д.).
        headers: Заголовки HTTP (если None, используется стандартный User-Agent).
    """
    if headers is None:
        headers = {
            'User-Agent': (
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/145.0.0.0 Safari/537.36'
            )
        }
    folder_path = Path(path)
    folder_path.mkdir(parents=True, exist_ok=True)
    if number_photo is None:
        full_path = folder_path / f"{name_photo}.jpeg"
    else:
        full_path = folder_path / f"{name_photo}_{number_photo}.jpeg"

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    full_path.write_bytes(response.content)
    return full_path


def main():
    """Запускает работу с API и сохраняет фото."""

    load_dotenv()
    name_photo = input("Введите название фото:").strip().lower()
    # spacex_id = '5eb87d42ffd86e000604b384'
    path = input("Введите путь: ").strip() or 'images/'
    api_key = os.getenv('NASA_ID')

    try:
        some_links = get_links_nasa(api_key)
        links_photo = ensure_list(some_links)
        # some_links = get_links_spacex(id=spacex_id)
        # links_photo = ensure_list(some_links)
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
