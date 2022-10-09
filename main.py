import os

from flask import Flask, render_template, request, flash, session, redirect, url_for, abort


app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(10)


@app.route('/')
def index():
    return render_template('index.html')


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
