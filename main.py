from flask import Flask, render_template, request


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/contact', methods=['POST'])
def contact():
    if request.method == 'POST':
        print(request.form)

    return render_template('contact.html')


if __name__ == "__main__":
    app.run(debug=True)
