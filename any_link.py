from pathlib import Path
from urllib.parse import urlsplit, unquote
from os.path import split, splitext
import requests


def get_extension(url):
    """Берет из ссылок расширение... 

    Args:
        url (str): Адрес картинки в интернете.

    Returns:
        str: Расширение файла (jpeg, gif и т.д.).
    """
    path, filename = split(unquote(urlsplit(url).path))
    name_photo, extension = splitext(filename)
    return extension


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


def download_image(url, name_photo, path, number_photo=None, headers=None):
    """Сохраняет картинку по URL в указанную папку.

    Возвращает путь к сохранённому файлу.

    Args:
        url (str): Адрес картинки в интернете.
        name_photo (str): Название фото.
        path (str): Папка для сохранения (будет создана, если нет).
        number_photo (int, optional): Номер фото для сохранения
            (если фото одно то сохранится по названию если,
             их несколько то название_1 и т.д.).
        headers (dict, optional): Заголовки HTTP (если None,
         используется стандартный User-Agent).

    Returns:
        Path: Путь к сохраненному файлу.
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
    extension = get_extension(url)
    if number_photo is None:
        full_path = folder_path / f"{name_photo}{extension}"
    else:
        full_path = folder_path / f"{name_photo}_{number_photo}{extension}"

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    full_path.write_bytes(response.content)
    return full_path


def main():
    """Запускает обработку ссылок и сохраняет фото."""
    url_input = input("Введите ссылку(и) через запятую: ").strip()
    some_links = [url.strip() for url in url_input.split(',') if url.strip()]
    for url in some_links:
        if not url.startswith(('http://', 'https://')):
            print(f"Ссылка '{url}' должна начинаться с http:// или https://")
            return
    name_photo = input("Введите название фото:").strip().lower()
    path = input("Введите путь или Enter:  ").strip() or 'images/'

    try:
        links_photo = ensure_list(some_links)
        if not links_photo:
            print("Фотографии не найдены.")
            return
        for number_links, link in enumerate(links_photo, start=1):
            number_photo = number_links if len(links_photo) > 1 else None
            saved_path = download_image(link, name_photo, path, number_photo)
            print(f"Файл сохранён: {saved_path}")
    except requests.exceptions.ReadTimeout:
        print("Превышено время ожидания...")
        return

    except requests.exceptions.ConnectionError as error:
        print(error, "Ошибка соединения")
        return

    except Exception as error:
        print(error, "ERROR_2")
        return


if __name__ == '__main__':
    main()
