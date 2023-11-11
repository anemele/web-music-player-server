import random
import socket
from itertools import chain
from pathlib import Path

from flask import Flask, render_template, send_file

app = Flask(__name__)

root = Path('D:/Music')
music_list = [
    music.name
    for music in chain.from_iterable(map(root.glob, '*.mp3,*.flac'.split(',')))
]


def rand_music():
    return random.choice(music_list)


@app.route('/')
def index():
    title = rand_music()
    data = dict(title=title, src=f'/music/{title}')
    return render_template('index.html', **data)


@app.route('/random')
def get_random():
    return rand_music()


@app.route('/music/<music>')
def get_music(music: str):
    return send_file(root / music)


if __name__ == '__main__':
    host = socket.gethostbyname(socket.gethostname())
    app.run(host=host, debug=False)
