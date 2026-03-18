import requests


def main():

    filename = 'hubble.jpeg'
    url = "https://upload.wikimedia.org/wikipedia/commons/3/3f/HST-SM4.jpeg"

    headers = {
        'User-Agent': (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
            'AppleWebKit/537.36 (KHTML, like Gecko)'
            'Chrome/145.0.0.0 Safari/537.36'
        )
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    with open(f"images/{filename}", 'wb') as file:
        file.write(response.content)


if __name__ == '__main__':
    main()
