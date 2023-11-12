import random
import socket
from itertools import chain, starmap
from pathlib import Path

from flask import Flask, render_template, send_file
from tinytag import TinyTag

app = Flask(__name__)


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
    items = ITEMS.copy()
    random.shuffle(items)
    data = dict(items=items)
    return render_template('index.html', **data)


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
