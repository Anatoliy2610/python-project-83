import validators
from bs4 import BeautifulSoup
import requests
from datetime  import date


def validate(url):
    if len(url) <= 255 and len(url) > 0 and validators.url(url):
        return True
    return False


def get_data_html(html_text):
    all_html = BeautifulSoup(html_text, 'html.parser')
    h1 = all_html.h1.string if all_html.h1 else ''
    title_text = all_html.find('title').string if all_html.find('title') else ''
    teg_meta = all_html.find_all('meta')
    description = ""
    for teg in teg_meta:
        if teg.get('name') == 'description':
            description = teg.get('content')
            break
    data = date.today()
    return h1, title_text, description, data

# response = requests.get('https://chat.hexlet.io')
# html = response.text
# all_html = BeautifulSoup(html, 'html.parser')
# print(get_data_html(html))
# print(get_data_html(html))
# print(all_html.h1)