from flask import (Flask, render_template,
                   request, redirect, url_for,
                   flash, get_flashed_messages)
import os
from dotenv import load_dotenv
from page_analyzer.validator import validate, get_data_url_checks
import requests
from page_analyzer import data


app = Flask(__name__)
load_dotenv()
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')


@app.route('/')
def index():
    return render_template('index.html')


@app.get('/urls')
def get_urls():
    conn = data.get_connect_db(app)
    data_urls = data.get_all_data_for_urls(conn)
    data.close(conn)
    return render_template('urls.html', data_urls=data_urls)


@app.post('/urls')
def post_urls():
    url = request.form['url']
    url_valid = validate(url)
    if url_valid:
        conn = data.get_connect_db(app)
        data_url = data.get_url_by_name(conn, url_valid)
        if not data_url:
            data.insert_url(conn, url_valid)
            new_data_url = data.get_url_by_name(conn, url_valid)
            data.close(conn)
            flash('Страница успешно добавлена', 'success')
            return redirect(url_for('get_urls_id', id=new_data_url.id))
        else:
            data.close(conn)
            flash('Страница уже существует', 'info')
            return redirect(url_for('get_urls_id', id=data_url.id))
    flash('Некорректный URL', 'danger')
    messages = get_flashed_messages(with_categories=True)
    return render_template('index.html', messages=messages, value=url), 422


@app.route('/urls/<int:id>')
def get_urls_id(id):
    try:
        conn = data.get_connect_db(app)
        all_data_url, last_data_url = data.get_data_url(conn, id)
        if not all_data_url:
            data.close(conn)
            return render_template('error_404.html'), 404
        else:
            messages = get_flashed_messages(with_categories=True)
            data.close(conn)
            return render_template('urls_id.html',
                                   all_data_url=all_data_url,
                                   last_data_url=last_data_url,
                                   messages=messages)
    except Exception:
        render_template('error_500.html'), 500


@app.post('/urls/<int:id>/checks')
def get_check_url(id):
    try:
        conn = data.get_connect_db(app)
        _, last_data_url = data.get_urls_with_checks(conn, id)
        data_checks = get_data_url_checks(last_data_url)
        data.insert_url_checks(conn, data_checks)
        data.close(conn)
        flash('Страница успешно проверена', 'success')
        return redirect(url_for('get_urls_id', id=id))
    except requests.exceptions.RequestException:
        flash('Произошла ошибка при проверке', 'danger')
        return redirect(url_for('get_urls_id', id=id))
