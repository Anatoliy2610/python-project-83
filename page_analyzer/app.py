from flask import (Flask, render_template,
                   request, redirect, url_for,
                   flash, get_flashed_messages)
import os
from dotenv import load_dotenv
from page_analyzer.validator import validate, get_data_html
import requests
from page_analyzer.data import (get_connect_db, close,
                                get_all_data_for_urls, add_data_db_urls,
                                get_data_url_for_urls, get_data_url,
                                add_data_db_url_checks)


app = Flask(__name__)
load_dotenv()
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')


@app.route('/')
def get_main_page():
    return render_template('main_page.html')


@app.get('/urls')
def get_urls():
    conn = get_connect_db(DATABASE_URL)
    data_urls = get_all_data_for_urls(conn)
    close(conn)
    return render_template('urls.html', data_urls=data_urls)


@app.post('/urls')
def post_urls():
    url = request.form['url']
    url_valid = validate(url)
    if url_valid:
        conn = get_connect_db(DATABASE_URL)
        data_url = get_data_url_for_urls(conn, url_valid)
        if not data_url:
            add_data_db_urls(conn, url_valid)
            data_urls = get_data_url_for_urls(conn, url_valid)
            close(conn)
            flash('Cтраница успешно добавлена', 'success')
            return redirect(url_for('get_urls_id', id=data_urls[0]))
        else:
            data_urls = get_data_url_for_urls(conn, url)
            close(conn)
            flash('Страница уже существует', 'info')
            return redirect(url_for('get_urls_id', id=data_urls[0]))
    flash('Некорректный URL', 'danger')
    messages = get_flashed_messages(with_categories=True)
    return render_template('main_page.html', messages=messages), 422


@app.route('/urls/<int:id>')
def get_urls_id(id):
    conn = get_connect_db(DATABASE_URL)
    all_data_url, last_data_url = get_data_url(conn, id)
    messages = get_flashed_messages(with_categories=True)
    close(conn)
    return render_template('urls_id.html',
                           all_data_url=all_data_url,
                           last_data_url=last_data_url,
                           messages=messages)


@app.post('/urls/<int:id>/checks')
def get_check_url(id):
    conn = get_connect_db(DATABASE_URL)
    _, last_data_url = get_data_url(conn, id)
    try:
        response = requests.get(last_data_url[1])
        response.raise_for_status()
    except requests.exceptions.RequestException:
        flash('Произошла ошибка при проверке', 'danger')
        return redirect(url_for('get_urls_id', id=id))
    status_code = response.status_code
    html_text = response.text
    h1, title_text, description = get_data_html(html_text)
    value = [last_data_url[0], status_code, h1, title_text, description]
    add_data_db_url_checks(conn, value)
    close(conn)
    flash('Страница успешно проверена', 'success')
    return redirect(url_for('get_urls_id', id=id))


@app.errorhandler(404)
def not_found(error):
    return render_template('error.html'), 404


@app.errorhandler(500)
def not_found(error):
    return render_template('error.html'), 500
