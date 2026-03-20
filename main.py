from dotenv import load_dotenv
from pathlib import Path
from urllib.parse import urlsplit, unquote
from os.path import split, splitext
import requests
import os
from pprint import pprint


def getting_extension(url):
    """Берет из ссылок расширение... 

    Args:
        url (str): Адрес картинки в интернете.

    Returns:
        (str): Расширение файла (jpeg, gif и т.д.).
    """
    path, filename = split(unquote(urlsplit(url).path))
    name_photo, extension = splitext(filename)
    return extension


def get_links_nasa(api_key=None, count=None, date=None, hd=False):
    """Получает список ссылок на изображения с NASA APOD API.

    Args:
        api_key (str, optional): API-ключ NASA. По умолчанию "DEMO_KEY".
        count (int, optional): Количество случайных изображений (1–100).
            Если указан, возвращает список случайных фото.
        date (str, optional): Дата в формате YYYY-MM-DD.
            Нельзя использовать вместе с count.
        hd (bool, optional): Если True, предпочитает HD-версию hdurl,
            но использует url как запасной вариант.

    Returns:
        list: Список строк с URL изображений.
            Может быть пустым, если ссылки не найдены.
    """
    if api_key is None:
        api_key = "DEMO_KEY"

    params = {'api_key': api_key}
    if count is not None:
        params['count'] = count
    if date is not None:
        params['date'] = date
    if hd:
        params['hd'] = True

    base_url = "https://api.nasa.gov/planetary/apod"
    response = requests.get(base_url, params=params)
    response.raise_for_status()

    apod_response = response.json()
    pprint(apod_response)
    if isinstance(apod_response, dict):
        apod_links = [apod_response]
    else:
        apod_links = apod_response

    some_links = []
    for apod_link in apod_links:
        if hd:
            some_link = apod_link.get('hdurl') or apod_link.get('url')
        else:
            some_link = apod_link.get('url')

        if some_link:
            some_links.append(some_link)

    return some_links


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


def ensure_list(some_links):
    """Приводит значение к списку для универсальной итерации.

    Делает из любого количества ссылок полученных от запроса - список

    Args:
        some_links: Необработанные ответы от других функций.

    Returns:
        list: Список ссылок даже если там одна ссылка,
        или пустой список.
    """
    if some_links is None:
        return []
    if isinstance(some_links, list):
        return some_links
    return [some_links]


# def download_image(url, name_photo, path, number_photo=None, headers=None):
#     """Сохраняет картинку по URL в указанную папку.

#     Возвращает путь к сохранённому файлу.

#     Args:
#         url(str): Адрес картинки в интернете.
#         name_photo(str): Название фото.
#         path(str): Папка для сохранения (будет создана, если нет).
#         number_photo(int, optional): Номер фото для сохранения
#             (если фото одно то сохранится по названию если,
#              их несколько то название_1 и т.д.).
#         headers(dict, optional): Заголовки HTTP (если None,
#          используется стандартный User-Agent).

#     Returns:
#         Path: Путь к сохраненному файлу.
#     """
#     if headers is None:
#         headers = {
#             'User-Agent': (
#                 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
#                 'AppleWebKit/537.36 (KHTML, like Gecko) '
#                 'Chrome/145.0.0.0 Safari/537.36'
#             )
#         }
#     folder_path = Path(path)
#     folder_path.mkdir(parents=True, exist_ok=True)
#     extension = getting_extension(url)
#     if number_photo is None:
#         full_path = folder_path / f"{name_photo}{extension}"
#     else:
#         full_path = folder_path / f"{name_photo}_{number_photo}{extension}"

#     response = requests.get(url, headers=headers)
#     response.raise_for_status()
#     full_path.write_bytes(response.content)
#     return full_path


def main():
    """Запускает работу с API и сохраняет фото."""

    load_dotenv()
    name_photo = input("Введите название фото:").strip().lower()
    # spacex_id = os.getenv('SPACEX_ID')
    api_key = os.getenv('NASA_ID')

    path = input("Введите путь: ").strip() or 'images/'
    try:
        some_links = get_links_nasa(api_key, count=30)
        links_photo = ensure_list(some_links)
        # some_links = get_links_spacex(spacex_id)
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
