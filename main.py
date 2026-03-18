from pathlib import Path
import requests


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
    links_foto = response.json().get('links', {}).get(
        'flickr', {}).get('original', [])
    return links_foto


def download_image(url, name_foto, path, number_link=None,  headers=None):
    """Сохраняет картинку по URL в указанную папку.

    Возвращает путь к сохранённому файлу.

    Args:
        url: Адрес картинки в интернете.
        name_foto: Название фото.
        path: Папка для сохранения (будет создана, если нет).
        number_link: Номер (индекс) ссылки.
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
    if number_link is None:
        full_path = folder_path / f"{name_foto}.jpeg"
    else:
        full_path = folder_path / f"{name_foto}_{number_link}.jpeg"

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    full_path.write_bytes(response.content)
    return full_path


def main():
    """Запускает работу с API и сохраняет фото."""
    name_foto = input("Введите название фото:").strip().lower()
    spacex_id = '5eb87d42ffd86e000604b384'
    path = (input("Введите путь: ").strip()
            or 'images/')
    try:
        links_foto = get_links_spacex(id=spacex_id)
    except requests.exceptions.ReadTimeout:
        print("Превышено время ожидания...")
        return

    except requests.exceptions.ConnectionError as error:
        print(error, "Ошибка соединения")
        return

    except Exception as error:
        print(error, "ERROR_2")
        return

    if not links_foto:
        print("Фотографии не найдены.")
        return
    if len(links_foto) == 1:
        saved_path = download_image(links_foto[0], name_foto, path)
        print(f"Файл сохранён: {saved_path}")
    else:
        for number, link in enumerate(links_foto, start=1):
            saved_path = download_image(link, name_foto, path, number)
            print(f"Файл сохранён: {saved_path}")


if __name__ == '__main__':
    main()
