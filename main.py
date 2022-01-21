import requests
import urllib
import os
from dotenv import load_dotenv





def get_incoming_url():
    try:
        long_url = input('Введите ссылку: ')
        response = requests.get(long_url)
        response.raise_for_status()
        return long_url
    except:
        print("Неверная ссылка!")
        exit()


def shorten_link(long_url, token):
    url = "https://api-ssl.bitly.com/v4/shorten"
    headers = {"Authorization": f"Bearer {token}"}
    body = {"long_url": long_url}
    response = requests.post(url, headers=headers, json=body)
    response.raise_for_status()
    return response.json()["id"]


def count_clicks(bitly_id, token):
    headers = {"Authorization": f"Bearer {token}"}
    info_url = f"https://api-ssl.bitly.com/v4/bitlinks/{bitly_id}/clicks/summary"
    response = requests.get(info_url, headers=headers)
    response.raise_for_status()
    return response.json()["total_clicks"]


def is_bitlink(url, token):
    try:
        headers = {"Authorization": f"Bearer {token}"}
        bitlink = urllib.parse.urlparse(url).netloc + \
                  urllib.parse.urlparse(url).path
        info_url = f"https://api-ssl.bitly.com/v4/bitlinks/{bitlink}"
        response = requests.get(info_url, headers=headers)
        response.raise_for_status()
        return True
    except:
        return False



if __name__ == "__main__":
    load_dotenv()
    BITLY_TOKEN = os.getenv('BITLY_TOKEN')

    incom_url = get_incoming_url()
    bitlink_detector = is_bitlink(incom_url)
    if bitlink_detector is True:
        bitlink_id = urllib.parse.urlparse(incom_url).netloc + \
                   urllib.parse.urlparse(incom_url).path
        result = count_clicks(bitlink_id, BITLY_TOKEN)
        print("Количество переходов по ссылке: ", result)
    else:
        result = shorten_link(incom_url, BITLY_TOKEN)
        print("Битлинк: ", result)
