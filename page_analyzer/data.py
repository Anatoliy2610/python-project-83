import psycopg2
from psycopg2.extras import NamedTupleCursor
from datetime import date


def get_connect_db(db_data):
    return psycopg2.connect(db_data)


def commit(conn):
    conn.commit()


def close(conn):
    conn.close()


def get_all_data_for_urls(conn):
    sql = '''SELECT
urls.id as id,
urls.name as name,
MAX(url_checks.created_at) as date,
url_checks.status_code as status
FROM urls
LEFT JOIN url_checks ON urls.id = url_checks.url_id
GROUP BY urls.id, urls.name, url_checks.status_code
ORDER BY urls.id DESC;'''
    with conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
        cursor.execute(sql)
        result = cursor.fetchall()
        commit(conn)
        return result


def get_data_url_for_urls(conn, url):
    sql = f"SELECT * FROM urls WHERE name='{url}';"
    with conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
        cursor.execute(sql)
        result = cursor.fetchone()
        commit(conn)
        return result


def get_data_url(conn, id):
    sql = f'''SELECT urls.id AS id, urls.name AS name,
urls.created_at AS date, url_checks.id AS id_checks,
url_checks.status_code AS status, url_checks.h1 AS h1,
url_checks.title AS title, url_checks.description AS description,
url_checks.created_at AS date_checks
FROM urls LEFT JOIN url_checks ON urls.id=url_checks.url_id
WHERE urls.id={id} ORDER BY id_checks DESC;'''
    with conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
        cursor.execute(sql)
        all_data = cursor.fetchall()
        commit(conn)
    with conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
        cursor.execute(sql)
        last_data = cursor.fetchone()
        commit(conn)
    return all_data, last_data


def add_data_db_urls(conn, value):
    sql = "INSERT INTO urls (name, created_at) VALUES (%s, %s);"
    new_date = date.today()
    with conn.cursor() as cursor:
        cursor.execute(sql, [value, new_date])
        commit(conn)


def add_data_db_url_checks(conn, value):
    sql = '''INSERT INTO url_checks
(url_id, status_code, h1, title, description, created_at)
VALUES (%s, %s, %s, %s, %s, %s);'''
    new_date = date.today()
    with conn.cursor() as cursor:
        cursor.execute(sql, (value + [new_date]))
        commit(conn)
