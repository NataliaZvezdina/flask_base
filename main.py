import os
import sqlite3
from flask import Flask, render_template, request, flash, session, redirect, url_for, abort, g
from FDataBase import FDataBase

DATABASE = '/tmp/fl_base.db'
DEBUG = True
SECRET_KEY = os.urandom(10)


app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(DATABASE=os.path.join(app.root_path, 'fl_base.db')))


def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def create_db():
    db = connect_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
        db.commit()
        db.close()


def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


@app.route('/')
def index():
    db = get_db()
    dbase = FDataBase(db)
    return render_template('index.html', menu=dbase.get_menu(), posts=dbase.get_posts_overview())


@app.route('/add_post', methods=['POST', 'GET'])
def add_post():
    db = get_db()
    dbase = FDataBase(db)

    if request.method == 'POST':
        if len(request.form['name']) > 4 and len(request.form['post']) > 10:
            res = dbase.add_post(request.form['name'], request.form['post'])
            if not res:
                flash('Error while adding post', category='error')
            else:
                flash('Post has been added successfully', category='success')
        else:
            flash('Error while adding post', category='error')

    return render_template('add_post.html', menu=dbase.get_menu())


@app.route('/post/<int:id_post>')
def show_post(id_post):
    db = get_db()
    dbase = FDataBase(db)
    title, post = dbase.get_post(id_post)
    if not title:
        abort(404)

    return render_template('post.html', menu=dbase.get_menu(), title=title, post=post)


@app.route('/contact', methods=['POST', 'GET'])
def contact():
    if request.method == 'POST':
        username = request.form['username']
        if len(username) > 2:
            flash('Message has been sent', category='success')
        else:
            flash('Error while sending', category='error')

    return render_template('contact.html')


@app.route('/profile/<username>')
def profile(username):
    if 'userLogged' not in session or session['userLogged'] != username:
        abort(401)
    return f'{username} profile'


@app.route('/login', methods=['POST', 'GET'])
def login():
    if 'userLogged' in session:
        return redirect(url_for('profile', username=session['userLogged']))
    elif request.method == 'POST' and request.form['username'] == 'test' and request.form['password'] == 'qwerty':
        session['userLogged'] = request.form['username']
        return redirect(url_for('profile', username=session['userLogged']))

    return render_template('login.html')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run(debug=True)
