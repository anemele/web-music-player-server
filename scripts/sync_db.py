from itertools import chain
from pathlib import Path

import requests
import tinytag


def read_music(path: Path) -> dict[str, str | float]:
    tag = tinytag.TinyTag.get(path)
    return {
        "title": tag.title or path.name,
        "artist": tag.artist or "<unknown>",
        "album": tag.album or "<unknown>",
        "duration": tag.duration or 0,
        "path": str(path),
    }


SUPPORTED_FORMAT = ["*.mp3", "*.flac"]


def get_music_files_from_fs(path: Path) -> set[Path]:
    it = chain.from_iterable(map(path.glob, SUPPORTED_FORMAT))
    return set(it)


url = "http://localhost:8000/api/music/"

sess = requests.Session()


def get_music_files_from_db() -> set[Path]:
    res = sess.get(url, params={"server": "true"})
    server_path_list = {item["path"] for item in res.json()}
    return set(map(Path, server_path_list))


def sync_db(path_fs: set[Path], path_db: set[Path]):
    to_post = path_fs - path_db
    to_delete = path_db - path_fs

    for path in to_post:
        print(f"to post {path}")
        sess.post(url, json=read_music(path))

    for path in to_delete:
        if path.exists():
            continue
        # Here requires the `id` field
        # f"{url}/{id}"
        print(f"to delete {path}")
        # sess.delete(url)


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    path_fs = get_music_files_from_fs(args.path)
    path_db = get_music_files_from_db()
    sync_db(path_fs, path_db)


if __name__ == "__main__":
    main()
