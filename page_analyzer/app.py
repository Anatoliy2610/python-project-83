from flask import Flask, render_template, request, redirect, url_for, flash, get_flashed_messages
import psycopg2
import os
from dotenv import load_dotenv
from page_analyzer.validator import validate, get_data_html
import requests
from page_analyzer.data import get_data_from_db, add_data_db
from datetime import date


app = Flask(__name__)
# app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SECRET_KEY'] = '1234121231'
load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
conn = psycopg2.connect(DATABASE_URL)


@app.route('/')
def get_main_page():
    return render_template('main_page.html')
# ещё нужно сделать, чтобы вводимый url не пропадал после нажатия кнопки

@app.get('/urls')
def get_urls():
    sql = '''SELECT urls.id, urls.name, MAX(url_checks.created_at), url_checks.status_code FROM urls 
LEFT JOIN url_checks
ON urls.id = url_checks.url_id
GROUP BY urls.id, urls.name, url_checks.status_code
ORDER BY urls.id DESC;'''
    urls = get_data_from_db(conn, sql, count_data='all')
    return render_template('urls.html', urls=urls)

@app.post('/urls')
def post_urls():
    if validate(request.form['url']):
        
         # берем информацию из тега form по name
        url = request.form['url']
        sql = f"select id from urls where name='{url}';"
        url_id = get_data_from_db(conn, sql)
        if not url_id:
            created_at = date.today()
            add_sql, value = "INSERT INTO urls (name, created_at) VALUES (%s, %s);", [str(url), str(created_at)]
            add_data_db(conn, add_sql, value)
            sql = f"select id from urls where name='{url}';"
            url_id = get_data_from_db(conn, sql)           
            # переходим на другую страницу по ID url
            flash('Cтраница успешно добавлена', 'info')
            # return render_template('urls.html')
            return redirect(url_for('get_urls_id', id=url_id[0]))
        else:
            flash('Страница уже существует', 'info')
            # return render_template('urls.html')
            return redirect(url_for('get_urls_id', id=url_id[0]))
    # флеш сообщение если некорректо ввели
    flash('Некорректный URL', 'danger')
    return render_template('main_page.html', value=request.form['url'])


@app.route('/urls/<int:id>')
def get_urls_id(id):

    sql = f"select id, name, created_at from urls where id={id} order by id desc;"
    id_from_urls, name_from_urls, date_from_urls = get_data_from_db(conn, sql)
    sql = f"select id, status_code, h1, title, description, created_at from url_checks where url_id={id} order by id desc;"
    data_from_url_checks = get_data_from_db(conn, sql, count_data='all')
    return render_template('urls_id.html',
                                    id_from_urls=id_from_urls,
                                    name_from_urls=name_from_urls,
                                    date_from_urls=date_from_urls,
                                    data_from_url_checks=data_from_url_checks)


@app.post('/urls/<int:id>/checks')
def get_check_url(id):
    # выбираем из БД urls -> id и name
    sql = f"SELECT id, name, created_at FROM urls where id={id};"
    id_from_urls, name_from_urls, date_from_urls = get_data_from_db(conn, sql)
    # проверяем проходит ли проверка адреса
    try:
        response = requests.get(name_from_urls)
        response.raise_for_status()
        status_code = response.status_code
    except requests.exceptions.RequestException:
        flash('Произошла ошибка при проверке', 'danger')
        return redirect(url_for('get_urls_id', id=id))
    sql = "INSERT INTO url_checks (url_id, status_code, h1, title, description, created_at) VALUES (%s, %s, %s, %s, %s, %s);"
    html_text = response.text
    h1, title_text, description, data = get_data_html(html_text)
    value = [id_from_urls, status_code, h1, title_text, description, data]
    add_data_db(conn, sql, value)
    sql = f"SELECT id, status_code, h1, title, description, created_at FROM url_checks WHERE url_id={id} order by id desc;"
    data_from_url_checks = get_data_from_db(conn, sql, 'all')
    flash('Страница успешно проверена', 'info')
    return render_template('urls_id.html', 
                                id_from_urls=id_from_urls, 
                                name_from_urls=name_from_urls, 
                                date_from_urls=date_from_urls,
                                data_from_url_checks=data_from_url_checks
                                )


if __name__ == '__main__':
    app.run(debug=True)

