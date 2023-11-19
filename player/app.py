import random
from functools import wraps
from pathlib import Path

from flask import Flask, jsonify, redirect, render_template, request, send_file, session

from .jobs import ITEMS, LENGTH

app = Flask(__name__)

app.secret_key = '789hdhfijbjnb4868ghjvh'

_PWD_PATH = Path('./pwd.txt')
if _PWD_PATH.exists():
    PASSWORD = _PWD_PATH.read_text().strip()
else:
    PASSWORD = None


def require_login(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('state') != 'login':
            return redirect('/login')
        return func(*args, **kwargs)

    return wrapper


@app.route('/')
@require_login
def index():
    return redirect('/music')


@app.get('/music')
@require_login
def get_music_page():
    items = ITEMS.copy()
    random.shuffle(items)
    data = dict(items=items)
    return render_template('index.html', **data)


@app.get('/login')
def get_login():
    return render_template('login.html')


@app.post('/login')
def post_login():
    # print(request.form) # POST
    # print(request.args) # GET

    if request.form.get('pwd') != PASSWORD:
        return jsonify(code=1, msg="ERROR_PASSWORD")

    session['state'] = 'login'
    return jsonify(code=0)


@app.route('/music/<int:id>')
@require_login
def get_music(id: int):
    if 0 <= id < LENGTH:
        return send_file(ITEMS[id]['path'])  # type: ignore
    return render_template('404.html')


def main():
    import socket

    host = socket.gethostbyname(socket.gethostname())
    app.run(host=host, debug=True)


if __name__ == '__main__':
    main()
