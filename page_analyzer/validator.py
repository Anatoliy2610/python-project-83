import validators
from bs4 import BeautifulSoup
from urllib.parse import urlparse


def validate(url):
    if len(url) <= 255 and len(url) > 0 and validators.url(url):
        url_parse = urlparse(url)
        return (url_parse.scheme + '://' + url_parse.netloc)
    return False


def check_data(value):
    if value is None:
        new_value = ''
    elif len(value) > 255:
        new_value = value[:255]
    return new_value


def get_data_html(html_text):
    all_html = BeautifulSoup(html_text, 'html.parser')
    h1 = all_html.h1.string if all_html.h1 else ''
    title = all_html.find('title').string if all_html.find('title') else ''
    teg_meta = all_html.find_all('meta')
    description = ""
    for teg in teg_meta:
        if teg.get('name') == 'description':
            description = teg.get('content')
            break
    return check_data(h1), check_data(title), check_data(description)
