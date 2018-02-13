import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
render_template, flash
import RPi.GPIO as GPIO
import pigpio
import numpy as np
import time
from light_control.transmitRF import transmit_code, transmit_outlet

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

@app.route('/outlet', methods=['POST'])
def outlet():
    code_dict = {1:['two_on','two_off'],2:['three_on','three_off'],3:['four_on','four_off']}
    out = [request.form['one'],request.form['two'],request.form['three']]
    print(request.form)
    on_arr = np.where([i=='on' for i in a])[0]
    off_arr = np.where([i=='off' for i in a])[0]
    if len(on_arr)==1:
        print(code_dict[on_arr])
        transmit_outlet(code_dict[on_arr][0])
    if len(off_arr)==1:
        print(code_dict[on_arr])
        transmit_outlet(code_dict[on_arr][1])
    return render_template('light_adjust.html',l_mode='light_controls')

@app.route('/a_on', methods=['POST'])
def a_on():
    transmit_outlet('two_on')
    return render_template('light_adjust.html',l_mode='light_controls')

@app.route('/a_off', methods=['POST'])
def a_off():
    transmit_outlet('two_off')
    return render_template('light_adjust.html',l_mode='light_controls')

@app.route('/outlet_2', methods=['POST'])
def outlet_2():
    if request.form['two'] == "On":
        transmit_outlet('two_on')
        return render_template('light_adjust.html',l_mode='light_controls')
    elif request.form['two'] == "Off":
        transmit_outlet('two_off')
        return render_template('light_adjust.html',l_mode='light_controls')
        
# @app.route('/b_off', methods=['POST'])
# def b_off():
#     transmit_code('two_off')
#     return render_template('light_adjust.html',l_mode='light_controls')

@app.route('/outlet_3', methods=['POST'])
def outlet_3():
    if request.form['three'] == "On":
        transmit_outlet('three_on')
        return render_template('light_adjust.html',l_mode='light_controls')
    elif request.form['three'] == "Off":
        transmit_outlet('three_off')
        return render_template('light_adjust.html',l_mode='light_controls')

# @app.route('/c_off', methods=['POST'])
# def c_off():
#     transmit_code('three_off')
#     return render_template('light_adjust.html',l_mode='light_controls')

@app.route('/outlet_4', methods=['POST'])
def outlet_4():
    if request.form['four'] == "On":
        transmit_outlet('four_on')
        return render_template('light_adjust.html',l_mode='light_controls')
    elif request.form['four'] == "Off":
        transmit_outlet('four_off')
        return render_template('light_adjust.html',l_mode='light_controls')

# @app.route('/d_off', methods=['POST'])
# def d_off():
#     transmit_code('four_off')
#     return render_template('light_adjust.html',l_mode='light_controls')

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
            radio = request.form['mode']
            if (radio=='ceiling') or (radio=='both'):
                pi1.set_PWM_dutycycle(5,new_colors[0])
                pi1.set_PWM_dutycycle(13,new_colors[1])
                pi1.set_PWM_dutycycle(26,new_colors[2])
                r = pi1.get_PWM_dutycycle(5)
                g = pi1.get_PWM_dutycycle(13)
                b = pi1.get_PWM_dutycycle(26)
            if (radio=='table') or (radio=='both'):
                pi1.set_PWM_dutycycle(17,new_colors[0])
                pi1.set_PWM_dutycycle(22,new_colors[1])
                pi1.set_PWM_dutycycle(18,new_colors[2])
                r = pi1.get_PWM_dutycycle(17)
                g = pi1.get_PWM_dutycycle(22)
                b = pi1.get_PWM_dutycycle(18)
            print(request.form)
        except (ValueError,AssertionError):
            flash('You need to type a value between 0 and 255 for all boxes')
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
