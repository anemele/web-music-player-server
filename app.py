import random
import socket
from itertools import chain, starmap
from pathlib import Path

from flask import Flask, redirect, render_template, request, send_file
from tinytag import TinyTag

app = Flask(__name__)

LOGIN: bool = False
PASSWORD = None
_PWD_PATH = Path('./pwd.txt')
if _PWD_PATH.exists():
    PASSWORD = _PWD_PATH.read_text().strip()


def find_music(root: Path, *ext):
    return (
        music for music in chain.from_iterable(map(root.glob, ext)) if music.is_file()
    )


def convert_duration(s: int) -> str:
    m, s = divmod(s, 60)
    if m < 60:
        return f'{m}:{s:02d}'
    h, m = divmod(m, 60)
    return f'{h}:{m:02d}:{s:02d}'


def get_item(id: int, path: Path):
    tag = TinyTag.get(path).as_dict()
    tag['id'] = id
    tag['path'] = path
    tag['duration'] = convert_duration(round(tag['duration']))
    if tag['title'] is None:
        tag['title'] = path.name
    return tag


_MUSIC_LIST = find_music(Path('D:/Music'), *'*.mp3,*.flac'.split(','))
ITEMS = list(starmap(get_item, enumerate(_MUSIC_LIST)))
LENGTH = len(ITEMS)


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
        return send_file(ITEMS[id]['path'])
    return render_template('404.html')


@app.route('/random')
def get_random():
    return str(ITEMS[random.randrange(LENGTH)]['id'])


if __name__ == '__main__':
    host = socket.gethostbyname(socket.gethostname())
    app.run(host=host, debug=True)
