from pathlib import Path
import requests


def main():

    filename = 'hubble.jpeg'
    folder_path = Path('images')
    folder_path.mkdir(parents=True, exist_ok=True)
    full_path = folder_path / filename

    url = "https://upload.wikimedia.org/wikipedia/commons/3/3f/HST-SM4.jpeg"

    headers = {
        'User-Agent': (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/145.0.0.0 Safari/537.36'
        )
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    # with open(full_path, 'wb') as file:
    #     file.write(response.content)
    full_path.write_bytes(response.content)


if __name__ == '__main__':
    main()
