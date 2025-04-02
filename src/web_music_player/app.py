import random

from flask import Flask, send_file
from flask_cors import CORS

from .core import load_data

data = load_data()
if data is None:
    exit(1)
item_list, id_path_map = data

app = Flask(__name__)
CORS(app)


@app.route("/api/list")
def get_music_list():
    random.shuffle(item_list)
    return item_list


@app.route("/api/music/<int:id>")
def get_music_file(id: int):
    return send_file(id_path_map[id])


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", type=int, default=5000)
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()

    app.run(
        host=args.host,
        port=args.port,
        debug=args.debug,  # default is False
    )


if __name__ == "__main__":
    main()
