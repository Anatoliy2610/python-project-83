# import sys
# import uuid
# from flask import session
import requests
from bs4 import BeautifulSoup
from datetime  import date


# name = 'https://ru.hexlet.io'
name = 'https://discord.com'
response = requests.get(name)
response.raise_for_status() # None
# print(response.status_code) # 200
# print(response.url) # https://ru.hexlet.io/
# print(response.headers) # словарь
# print(response.)
# a = response.headers
# for item in a:
#     print (item)
# from lxml.html import fromstring

# print (date.today())
# # вот так!
# a = response.text
# # print(a[a.find('<title>') + 7 : a.find('</title>')])

# all_teg = BeautifulSoup(a, 'html.parser')
# print(type(all_teg))
# res = soup.find_all("meta")
# des = ''
# for item in res:
#     if item.get('name') == 'description':
#         des = item.get('content')
#         break
# print(des)
# soup.find_all("meta")

# def titles (text):
#     i = 0
#     value = '<title>'
#     value2 = '</title>'
#     while i < len(text):
#         new_text = text[i:(i+500)]
#         if value in new_text and value2 in new_text:
#             ind = 0

#             i = len(text)
#             # while ind < len(new_text):
        
#         i += 200

        
# titles(a)
# print(len('<title>Хекслет — онлайн-школа программирования, онлайн-обучение ИТ-профессиям</title>'))



    # value2 = '</title>'
    # while i < len(a):
    #     if value == a[i:(i+len(value))]:
    #         i = len(a)
    #         return(a[(i + len(value) + 1) : ])
    #     else:
    #         i += 1

# print(val in a)

# print(len(a))



# >>> hearders = {'headers':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:51.0) Gecko/20100101 Firefox/51.0'}
# >>> n = requests.get('http://www.imdb.com/title/tt0108778/', headers=hearders)
# >>> al = n.text
# >>> al[al.find('<title>') + 7 : al.find('</title>')]
# u'Friends (TV Series 1994\u20132004) - IMDb'


# Date
# Content-Type
# Transfer-Encoding
# Connection
# vary
# x-xss-protection
# x-content-type-options
# x-permitted-cross-domain-policies
# referrer-policy
# strict-transport-security
# link
# etag
# cache-control
# set-cookie
# x-request-id
# x-runtime
# x-frame-options
# x-time
# content-encoding
# CF-Cache-Status
# Report-To
# NEL
# Server
# CF-RAY
# alt-svc

# class Repository:
#     def content(self):
#         return session.values()

#     def find(self, id):
#         try:
#             return session[id]
#         except KeyError:
#             sys.stderr.write(f'Wrong item id: {id}')
#             raise

#     def save(self, item):
#         item['id'] = str(uuid.uuid4())
#         session[item['id']] = item


# #111111111111111111
# from flask import Flask, render_template, redirect, request
# from validator import validate
# import os
# from data import Repository
# import psycopg2
# from dotenv import load_dotenv


# app = Flask(__name__)
# app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# load_dotenv()
# DATABASE_URL = os.getenv('DATABASE_URL')
# conn = psycopg2.connect(DATABASE_URL)


from flask import Flask, render_template, request, redirect, get_flashed_messages, flash, session
import psycopg2
import os
from dotenv import load_dotenv
from page_analyzer.validator import validate
import requests
from page_analyzer.data import get_data_from_db, add_data_db


app = Flask(__name__)
# app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SECRET_KEY'] = '1234121231'
load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
conn = psycopg2.connect(DATABASE_URL)

# SELECT TOP 1 * FROM Table ORDER BY ID DESC

# sql = '''SELECT ur.id, 
# ur.name, 
# ur.created_at, 
# ch.status_code 
# FROM urls AS ur 
# INNER JOIN url_checks AS ch 
# ON ur.id = ch.url_id 
# WHERE ur.created_at = (SELECT created_at FROM url_checks ORDER BY url_checks DESC LIMIT 1)
# ORDER BY ur.id desc;
# '''
# sql = "SELECT url_id, max(created_at) from url_checks group by url_id;"

sql = '''SELECT urls.id, urls.name, MAX(url_checks.created_at), url_checks.status_code FROM urls 
LEFT JOIN url_checks
ON urls.id = url_checks.url_id
GROUP BY urls.id, urls.name, url_checks.status_code
ORDER BY urls.id DESC;'''
# sql = 'SELECT created_at FROM url_checks ORDER BY url_checks DESC LIMIT 1;'
# sql = 'select distinct url_id, created_at from url_checks;'
# sql = '''SELECT url_id, created_at FROM (SELECT url_id, created_at, ROW_NUMBER() OVER (PARTITION BY url_id ORDER BY created_at DESC) as rn FROM url_checks) WHERE rn = 1;'''
urls = get_data_from_db(conn, sql, count_data='all')
res = []
for item in urls:
    for i in item:
        if i:
            i = ''
print(urls)


def func():
    sql1 = "select id from urls order by id desc;" # [(7,), (6,), (5,), (4,), (3,), (2,), (1,)]
    ids_urls = get_data_from_db(conn, sql1, count_data='all')
    sql2 = "SELECT DISTINCT url_id from url_checks;"
    ids_checks = get_data_from_db(conn, sql2, count_data='all') # [(6,), (1,), (5,), (2,)]
    res = []
    for item in ids_urls:
        if item not in ids_checks:
            res.append(item)
    # for item in res:




# (1, 'https://ru.hexlet.io', datetime.date(2024, 8, 27))
# (2, 'https://ru.hexlet.ioasd', datetime.date(2024, 8, 27))
# (3, 'https://ru.hexlet.ioqwe', datetime.date(2024, 8, 27))
# (4, 'https://ru.hexlet.iasdo', datetime.date(2024, 8, 28))
# (5, 'https://chat.hexlet.io', datetime.date(2024, 8, 28))
# (6, 'https://yandex.ru', datetime.date(2024, 8, 28))
# (7, 'https://yandex.ruqwe', datetime.date(2024, 8, 28))









# sql = f"select id, name, created_at from urls where id=10;"
# id_url_urls, name_url_urls, date_url_urls = get_data_from_db(conn, sql)
# # id_url, name = get_data_from_db(conn, sql)
# print([name_url_urls])

# @app.route('/')
# def index():
#     return render_template('main_page.html')


# @app.get('/s1')
# def get_list_sites():
#     return render_template(
#         'sites/list_sites.html'
#         )


# @app.route('/s2')
# def get_check_sites():
#     return render_template('sites/check_sites.html')


# @app.errorhandler(404)
# def not_found(error):
#     return 'Oops! 404', 404


# @app.errorhandler(405)
# def not_found(error):
#     return 'Oops! 405', 405


# if __name__ == '__main__':
#     app.run()

