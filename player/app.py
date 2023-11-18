import random
from pathlib import Path

from flask import Flask, redirect, render_template, request, send_file

from .jobs import ITEMS, LENGTH

app = Flask(__name__)

LOGIN: bool = False
PASSWORD = None
_PWD_PATH = Path('./pwd.txt')
if _PWD_PATH.exists():
    PASSWORD = _PWD_PATH.read_text().strip()


@app.route('/')
def index():
    global LOGIN
    if PASSWORD is not None and not LOGIN:
        return redirect('/login')
    LOGIN = False

    items = ITEMS.copy()
    random.shuffle(items)
    data = dict(items=items)
    return render_template('index.html', **data)


@app.route('/login')
def get_login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def post_login():
    global LOGIN
    # print(request.form) # POST
    # print(request.args) # GET

    if request.form.get('pwd') != PASSWORD:
        return dict(code=1)

    LOGIN = True
    return dict(code=0)


@app.route('/music/<int:id>')
def get_music(id: int):
    if 0 <= id < LENGTH:
        return send_file(ITEMS[id]['path'])  # type: ignore
    return render_template('404.html')


@app.route('/random')
def get_random():
    return str(ITEMS[random.randrange(LENGTH)]['id'])


def main():
    import socket

    host = socket.gethostbyname(socket.gethostname())
    app.run(host=host, debug=True)


if __name__ == '__main__':
    main()
