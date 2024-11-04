import flask
from flask import (request, jsonify, redirect, url_for,
                   render_template, make_response)
import pytz
from datetime import datetime
from forms import UserForm
import sqlite3
from concurrent.futures import ThreadPoolExecutor
from uuid import uuid4
import logging
import os

logging.basicConfig(level=logging.DEBUG)

def create_table():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users_mk (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            UUID TEXT NOT NULL,
            fam_child TEXT NOT NULL,
            name_child TEXT NOT NULL,
            otch_child TEXT NOT NULL,
            date_birth TEXT NOT NULL,
            name_parent TEXT NOT NULL,
            phone_parent TEXT NOT NULL,
            tg_account TEXT,
            platform TEXT,
            mk_day TEXT,
            mk_time TEXT,
            mk_name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
    ''')
    conn.commit()
    conn.close()
app = flask.Flask(__name__)
app.config['SECRET_KEY'] = 'efimfesifmsomfseifmesimfesfm'

db_folder = os.path.join(os.getcwd(), 'dbfolder')
if not os.path.exists(db_folder):
    os.makedirs(db_folder)

db_name_file = 'database.db'
db_name = os.path.join(os.getcwd(), 'dbfolder', db_name_file)
create_table()

@app.route('/', methods=['GET'])
def home_main():
    if request.cookies.get('UUID'):
        #logging.debug(f"UUID: {request.cookies.get('UUIDDD'), request.cookies.keys()}")
        response = make_response(render_template('home.html', **{'p_title': 'Мастер-Класс Алгоритмика Сахалин'}))
        return response
    else:
        user_id = str(uuid4())
        #logging.debug(f"UUID: {user_id}")
        response = make_response(render_template('home.html', **{'p_title': 'Мастер-Класс Алгоритмика Сахалин'}))
        response.set_cookie('UUID', user_id, max_age=60*60*24+30)
        #logging.debug(f"Set-Cookie header: {response.headers.get('Set-Cookie')}")
        return response

@app.route('/add_mk', methods=['GET', 'POST'])
def add_mk():
    form = UserForm()

    form.mk_day.choices = [('Среда', 'Среда'), ('Суббота', 'Суббота'), ('Воскресенье', 'Воскресенье')]
    form.mk_time.choices = [('10:00', '10:00'), ('14:00', '14:00'), ('16:00', '16:00')]
    form.mk_name.choices = [('Мастер-класс по Scratch', 'Визуальное программирование'),
                            ('Основы логики и программирования', 'Подготовка к школе(Основы логики и программирования)'),
                            ('Программирование в Minecraft', 'Программирование в Minecraft'),
                            ('Мастер-класс по Python', 'Мастер-класс по Python'),
                            ('Мастер-класс по Web', 'Мастер-класс по Web')]

    if not request.cookies.get('UUID'):
        return redirect(url_for('home_main'))

    logging.debug(f"Data {form.data}")


    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                conn = sqlite3.connect(db_name)
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO users_mk (UUID, fam_child, name_child, otch_child, date_birth, name_parent, 
                    phone_parent, tg_account, platform, mk_day, mk_time, mk_name)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (request.cookies.get('UUID'), form.fam_child.data, form.name_child.data,
                      form.otch_child.data, form.date_birth.data, form.name_parent.data,
                      form.phone_parent.data, form.tg_account.data, request.headers.get('Sec-Ch-Ua-Platform'),
                        form.mk_day.data, form.mk_time.data, form.mk_name.data
                      ))
                conn.commit()
                conn.close()
                logging.debug("Data inserted successfully in DB")
                return redirect(url_for('home_main'))
            except Exception as e:
                logging.error(f"Error inserting data: {e}")
        else:
            logging.debug(f"Form validation failed: {form.errors}\n"
                          f"Form data: {form.data}")
    return render_template('mk.html', form=form, p_title='Запись на мастер-класс')



@app.route('/kontakti', methods=['GET'])
def kontakti():
    response = make_response(render_template('contact.html', **{'p_title': 'Контакты'}))
    return response


@app.route('/about', methods=['GET'])
def about():
    response = make_response(render_template('about.html', **{'p_title': 'О нас и не только'}))
    return response


@app.route('/special_page', methods=['GET'])
def special_page():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''SELECT fam_child, name_child, mk_name, mk_day, mk_time, created_at
                   FROM users_mk
                   WHERE UUID = ?''', (str(request.cookies.get('UUID')),))
    users = cursor.fetchall()
    conn.close()
    #logging.debug(f"Users: {users}")
    response = make_response(render_template('special_page.html',
                                             **{'p_title': 'Мои заявки', 'users': users}))
    return response



if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app.run(debug=True, port=5000)