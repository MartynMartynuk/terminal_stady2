import requests
import urllib
import os
from dotenv import load_dotenv
from pathlib import Path


env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)

TOKEN = os.getenv('TOKEN')


def input_func():
    try:
        long_url = input('Введите ссылку: ')
        test_response = requests.get(long_url)
        test_response.raise_for_status()
        return long_url
    except:
        return "Неверная ссылка\n", "Ошибка! Код ответа:", \
               test_response.status_code


def shorten_link(long_url, token=TOKEN):
    url = "https://api-ssl.bitly.com/v4/shorten"
    headers = {"Authorization": f"Bearer {token}"}
    body = {"long_url": long_url}
    response = requests.post(url, headers=headers, json=body)
    response.raise_for_status()
    return "Битлинк", response.json()["id"]


def count_clicks(bitly_id, token=TOKEN):
    headers = {"Authorization": f"Bearer {token}"}
    info_url = f"https://api-ssl.bitly.com/v4/bitlinks/{bitly_id}/clicks/summary"
    response = requests.get(info_url, headers=headers)
    response.raise_for_status()
    return "Количество переходов по ссылке", response.json()["total_clicks"]


def is_bitlynk(url):
    if urllib.parse.urlparse(url).netloc == "bit.ly":
        bitly_id = urllib.parse.urlparse(url).netloc +\
                   urllib.parse.urlparse(url).path
        return count_clicks(bitly_id)
    else:
        return shorten_link(url)


if __name__ == "__main__":
    result = is_bitlynk(input_func())
    print(f"{result[0]}: {result[1]}")
