from utils import ensure_list, download_image
from dotenv import load_dotenv
from datetime import datetime
import requests
import os


def get_links_nasa_epic(api_key=None, date=None):
    """Получает список ссылок на изображения с NASA EPIC API.

    Args:
        api_key (str, optional): API-ключ NASA. По умолчанию "DEMO_KEY".
        date (str, optional): Дата в формате YYYY-MM-DD.

    Returns:
        list: Список строк с URL изображений.
            Может быть пустым, если ссылки не найдены.
    """
    if api_key is None:
        api_key = "DEMO_KEY"

    params = {'api_key': api_key}

    if date:
        base_url = f"https://api.nasa.gov/EPIC/api/natural/images/date/{date}"
    else:
        base_url = "https://api.nasa.gov/EPIC/api/natural/images"

    response = requests.get(base_url, params=params)
    response.raise_for_status()
    epic_response = response.json()

    some_links = []
    base_photo_url = "https://api.nasa.gov/EPIC/archive/natural/"
    for epic_link in epic_response:
        date_str = epic_link['date'].split()[0].replace('-', '/')
        name_photo = epic_link['image']

        photo_url = f"{base_photo_url}{date_str}/png/{name_photo}.png"

        some_links.append(photo_url)

    return some_links


def main():
    """Запускает работу с API и сохраняет фото."""
    load_dotenv()
    data_input = input("Введите дату (YYYY-MM-DD) или Enter: ").strip()
    if not data_input:
        date = None
    else:
        try:
            date = datetime.strptime(
                data_input, "%Y-%m-%d").strftime("%Y-%m-%d")
        except ValueError:
            print("Неверный формат даты. Нужно YYYY-MM-DD.")
            return
    api_key = os.getenv('NASA_ID')
    name_photo = input("Введите название фото: ").strip().lower()
    path = input("Введите путь или Enter: ").strip() or 'images/'

    some_links = None
    try:
        some_links = get_links_nasa_apod(api_key, count, date, hd)

    except requests.exceptions.RequestException as error:
        print(f"Ошибка запроса к NASA EPIC API: {error}")
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
