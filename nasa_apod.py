from utils import ensure_list, download_image
from dotenv import load_dotenv
from datetime import datetime
import requests
import os


def get_links_nasa_apod(api_key=None, count=None, date=None, hd=False):
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

    if isinstance(apod_response, dict):
        apod_links = [apod_response]
    else:
        apod_links = apod_response

    some_links = []
    for apod_link in apod_links:
        if apod_link.get('media_type') != 'image':
            continue

        if hd:
            some_link = apod_link.get('hdurl') or apod_link.get('url')
        else:
            some_link = apod_link.get('url')

        if some_link:
            some_links.append(some_link)
    return some_links


def main():
    """Запускает работу с API и сохраняет фото."""

    load_dotenv()
    count_input = input("Введите количество (1-100) или Enter: ").strip()
    if count_input:
        try:
            count = int(count_input)
            if not (1 <= count <= 100):
                print("Количество должно быть от 1 до 100.")
                return
            date = None
        except ValueError:
            print("Неверное число.")
            return
    else:
        count = None
        date_input = input("Введите дату (YYYY-MM-DD) или Enter: ").strip()
        if date_input:
            try:
                date = datetime.strptime(
                    date_input, "%Y-%m-%d").strftime("%Y-%m-%d")
            except ValueError:
                print("Неверный формат даты. Нужно YYYY-MM-DD.")
                return
        else:
            date = None

    hd_input = input("HD-версия? (y/n): ").strip().lower()
    hd = hd_input == 'y'

    api_key = os.getenv('NASA_ID')

    name_photo = input("Введите название фото: ").strip().lower()
    path = input("Введите путь или Enter: ").strip() or 'images/'

    some_links = None
    try:
        some_links = get_links_nasa_apod(api_key, count, date, hd)

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
