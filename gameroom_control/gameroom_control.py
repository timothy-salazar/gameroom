import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
render_template, flash
import RPi.GPIO as GPIO
import pigpio
import numpy as np
import time
from light_control.transmitRF import transmit_code, transmit_code_et

app = Flask(__name__) # create the application instance :)
app.config.from_object(__name__) # load config from this file , flaskr.py

# Load default config and override config from an environment variable
app.config.update(dict(
DATABASE=os.path.join(app.root_path, 'flaskr.db'),
SECRET_KEY='development key',
USERNAME='admin',
PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
pi1 = pigpio.pi()

# def transmit_code(a):
#     print(a)
#
# def transmit_code_et(a):
#     print(a)
#
# @app.route('/a_on')
# def a_on():
#     transmit_code('a_on')
#     return render_template('layout.html')
#
# @app.route('/a_off')
# def a_off():
#     transmit_code('a_off')
#     return render_template('layout.html')
#
# @app.route('/red_on')
# def red_on():
#     transmit_code_et('two_on')
#     return render_template('layout.html')
#
# @app.route('/red_off')
# def red_off():
#     transmit_code_et('two_off')
#     return render_template('layout.html')

# @app.route('/change_ceiling',methods=['GET','POST'])
# def change_ceiling():
#     if request.method == 'POST':
#         if not session.get('logged_in'):
#             abort(401)
#         try:
#             new_colors = np.array([request.form['red'],request.form['green'],request.form['blue']])
#             new_colors = new_colors.astype('int')
#             assert np.all(new_colors<256)
#             assert np.all(new_colors>=0)
#             # pi1.set_PWM_dutycycle(5,new_colors[0])
#             # pi1.set_PWM_dutycycle(13,new_colors[1])
#             # pi1.set_PWM_dutycycle(26,new_colors[2])
#             print(new_colors)
#         except (ValueError,AssertionError):
#             flash('You need to type a value between 0 and 255 for all boxes')
#     return render_template('light_adjust.html',l_mode = 'change_ceiling')

# @app.route('/color_wheel',methods=['GET','POST'])
# def color_wheel():
#     if request.method == 'POST':
#         if not session.get('logged_in'):
#             abort(401)
#         try:
#             print(request.form)
#             print(len(request.form))
#             for i in request.form.items():
#                 print(i)
#             h = request.form['ceiling'].lstrip('#')
#             print(print('RGB =', tuple(int(h[i:i+2], 16) for i in (0, 2 ,4))))
#             h = request.form['table'].lstrip('#')
#             print(print('RGB =', tuple(int(h[i:i+2], 16) for i in (0, 2 ,4))))
#             # new_colors = np.array([request.form['red'],request.form['green'],request.form['blue']])
#             # new_colors = new_colors.astype('int')
#             # assert np.all(new_colors<256)
#             # assert np.all(new_colors>=0)
#             # pi1.set_PWM_dutycycle(5,new_colors[0])
#             # pi1.set_PWM_dutycycle(13,new_colors[1])
#             # pi1.set_PWM_dutycycle(26,new_colors[2])
#             #print(new_colors)
#             return render_template('light_adjust.html',l_mode = 'change_ceiling')
#         except (ValueError,AssertionError):
#             flash('You need to type a value between 0 and 255 for all boxes')
#     return render_template('light_adjust.html',l_mode = 'change_ceiling')

# @app.route('/change_table',methods=['GET','POST'])
# def change_table():
#     if request.method == 'POST':
#         if not session.get('logged_in'):
#             abort(401)
#             try:
#                 new_colors = np.array([request.form['red'],request.form['green'],request.form['blue']])
#                 new_colors = new_colors.astype('int')
#                 assert (np.all(new_colors<256) and np.all(new_colors>=0))
#                 # pi1.set_PWM_dutycycle(17,new_colors[0])
#                 # pi1.set_PWM_dutycycle(22,new_colors[1])
#                 # pi1.set_PWM_dutycycle(18,new_colors[2])
#                 print(new_colors)
#             except (ValueError,AssertionError):
#                 flash('You need to type a value between 0 and 255 for all boxes')
#                 return render_template('light_adjust.html',l_mode='change_table')

# @app.route('/change_both',methods=['GET','POST'])
# def change_both():
#     if request.method == 'POST':
#         if not session.get('logged_in'):
#             abort(401)
#             try:
#                 new_colors = np.array([request.form['red'],request.form['green'],request.form['blue']])
#                 new_colors = new_colors.astype('int')
#                 assert (np.all(new_colors<256) and np.all(new_colors>=0))
#                 # pi1.set_PWM_dutycycle(5,new_colors[0])
#                 # pi1.set_PWM_dutycycle(13,new_colors[1])
#                 # pi1.set_PWM_dutycycle(26,new_colors[2])
#                 # pi1.set_PWM_dutycycle(17,new_colors[0])
#                 # pi1.set_PWM_dutycycle(22,new_colors[1])
#                 # pi1.set_PWM_dutycycle(18,new_colors[2])
#                 print(new_colors)
#             except (ValueError,AssertionError):
#                 flash('You need to type a value between 0 and 255 for all boxes')
#                 return render_template('light_adjust.html',l_mode='change_both')
#
@app.route('/a_on')
def a_on():
    transmit_code('a_on')
    return render_template('light_adjust.html',l_mode='light_controls')

@app.route('/a_off')
def a_off():
    transmit_code('a_off')
    return render_template('light_adjust.html',l_mode='light_controls')

@app.route('/', methods=['GET','POST'])
def light_controls():
    r = 0
    g = 0
    b = 0
    if request.method == 'POST':
        if not session.get('logged_in'):
            abort(401)
        try:
            new_colors = np.array([request.form['red'],request.form['green'],request.form['blue']])
            new_colors = new_colors.astype('int')
            assert (np.all(new_colors<256) and np.all(new_colors>=0))
            r = request.form['mode']
            if (r=='ceiling') or (r=='both'):
                pi1.set_PWM_dutycycle(5,new_colors[0])
                pi1.set_PWM_dutycycle(13,new_colors[1])
                pi1.set_PWM_dutycycle(26,new_colors[2])
                r = pi1.get_PWM_dutycycle(5)
                g = pi1.get_PWM_dutycycle(13)
                b = pi1.get_PWM_dutycycle(26)
            if (r=='table') or (r=='both'):
                pi1.set_PWM_dutycycle(17,new_colors[0])
                pi1.set_PWM_dutycycle(22,new_colors[1])
                pi1.set_PWM_dutycycle(18,new_colors[2])
                r = pi1.get_PWM_dutycycle(17)
                g = pi1.get_PWM_dutycycle(22)
                b = pi1.get_PWM_dutycycle(28)
            print(request.form)
        except (ValueError,AssertionError):
            flash('You need to type a value between 0 and 255 for all boxes')
            #return render_template('light_adjust.html',l_mode='change_both')
    return render_template('light_adjust.html',l_mode='light_controls',r_value=r,g_value=g,b_value=b)

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
        db = get_db()
        db.execute('insert into entries (title, text) values (?, ?)',
        [request.form['title'], request.form['text']])
        db.commit()
        flash('New entry was successfully posted')
        return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
        return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
        return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
        db.commit()

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')
