from any_link.py import ensure_list, download_image
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
    api_key = None  # os.getenv('NASA_ID')
    name_photo = input("Введите название фото:").strip().lower()
    path = input("Введите путь или Enter:  ").strip() or 'images/'
    try:
        some_links = get_links_nasa_apod(api_key, date)
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
    for number_links, link in enumerate(links_photo, start=0):
        number_photo = number_links if len(links_photo) > 1 else None
        saved_path = download_image(link, name_photo, path, number_photo)
        print(f"Файл сохранён: {saved_path}")


if __name__ == '__main__':
    main()
