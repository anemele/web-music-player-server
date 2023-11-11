import random
import socket
from itertools import chain
from pathlib import Path

from flask import Flask, redirect, render_template, send_file

app = Flask(__name__)

root = Path('D:/Music')
music_list = [
    music.name
    for music in chain.from_iterable(map(root.glob, '*.mp3,*.flac'.split(',')))
]
lens = len(music_list)


def rand():
    return random.randrange(lens)


@app.route('/')
def index():
    return redirect(f'/page/{rand()}')


@app.route('/page/<int:id>')
def get_page(id):
    next_id = rand()
    data = dict(music=music_list[id], next=dict(id=next_id, name=music_list[next_id]))
    return render_template('index.html', **data)


@app.route('/music/<music>')
def get_music(music: str):
    return send_file(root / music)


if __name__ == '__main__':
    host = socket.gethostbyname(socket.gethostname())
    app.run(host=host, debug=True)
