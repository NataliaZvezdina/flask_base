import os

from flask import Flask, render_template, request, flash


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


if __name__ == "__main__":
    app.run(debug=True)
