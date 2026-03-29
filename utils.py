from pathlib import Path
from os.path import split, splitext
from urllib.parse import urlsplit, unquote
import argparse
import requests


def add_common_args(parser):
    """Добавляет общие аргументы для скриптов загрузки изображений."""
    parser.add_argument(
        '-n', '--name',
        help=("Имя файла (без расширения)."
              "По умолчанию извлекается из URL")
    )
    parser.add_argument(
        '-p', '--path',
        default='images',
        help='Папка для сохранения (по умолчанию images)'
    )
    return parser


def get_filename(url):
    """Берет из ссылок расширение... 

    Args:
        url (str): Адрес картинки в интернете.

    Returns:
        str: Расширение файла (jpeg, gif и т.д.).
    """
    path, filename = split(unquote(urlsplit(url).path))
    name_photo, extension = splitext(filename)
    if not extension:
        extension = ".jpeg"
    return name_photo, extension


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


def download_image(
    url,
    name_photo=None,
    path='images',
    number_photo=None,
    headers=None
):
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

    name_from_url, extension = get_filename(url)

    if name_photo:
        final_name = name_photo
    elif name_from_url:
        final_name = name_from_url
    else:
        final_name = "noname"

    if number_photo is None:
        full_path = folder_path / f"{final_name}{extension}"
    else:
        full_path = folder_path / f"{final_name}_{number_photo}{extension}"

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    full_path.write_bytes(response.content)
    return full_path
