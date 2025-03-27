from flask import Flask, send_file

from .core import load_data

item_list, id_path_map, server_config = load_data()
legnth = len(id_path_map)

app = Flask(__name__)

app.secret_key = "789hdhfijbjnb4868ghjvh"


@app.route("/api/list")
def get_music_list():
    return item_list


@app.route("/api/music/<int:id>")
def get_music_file(id: int):
    return send_file(id_path_map[id])


def main():
    app.run(
        debug=server_config.debug,
        host=server_config.host,
        port=server_config.port,
    )
