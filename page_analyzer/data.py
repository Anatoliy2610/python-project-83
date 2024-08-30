import psycopg2
import os
from dotenv import load_dotenv
import validators
import requests


load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
conn = psycopg2.connect(DATABASE_URL)

def get_data_from_db(conn, req, count_data='one'):
    with conn.cursor() as cursor:
    # взять данные из БД
        cursor.execute(req)
        if count_data == 'one':
            last_req = cursor.fetchone()
            conn.commit()
            return last_req
        req = cursor.fetchall()
        conn.commit()
        return req


def add_data_db(conn, req, value):
    with conn.cursor() as cursor:
        # внести данные в БД
        cursor.execute(req, value)
        conn.commit()



# sql = f"select id, name, created_at from urls where id=1;"
# id_url = get_data_from_db(conn, sql)
# print(id_url)

# sql = f"select url_id, status_code, h1, title, description, created_at from url_checks;"

# with conn.cursor() as cursor:
#     # взять данные из БД
#     cursor.execute(f"select * from test;")

#     req = cursor.fetchall()
#     conn.commit()
#     print (req)
sql = "INSERT INTO url_checks (url_id, status_code, h1, title, description, created_at) VALUES (%s, %s, %s, %s, %s, %s);"
value = [2, 400, 'asdsad', 'title_text', 'description', '2024-08-27']
add_data_db(conn, sql, value)