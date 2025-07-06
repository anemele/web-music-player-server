from collections.abc import Mapping, Set
from itertools import chain
from pathlib import Path

import requests
import tinytag


def read_music(path: Path) -> Mapping[str, str | float]:
    tag = tinytag.TinyTag.get(path)
    return {
        "title": tag.title or path.name,
        "artist": tag.artist or "<unknown>",
        "album": tag.album or "<unknown>",
        "duration": tag.duration or 0,
        "path": str(path),
    }


SUPPORTED_FORMAT = ["*.mp3", "*.flac"]


def get_music_files_from_fs(path: Path) -> Set[Path]:
    it = map(path.glob, SUPPORTED_FORMAT)
    it = chain.from_iterable(it)
    return set(it)


url = "http://127.0.0.1:8000/api/music/"

sess = requests.Session()


def get_music_files_from_db() -> Mapping[Path, int]:
    res = sess.get(url, params={"server": "true"})
    ret = {Path(item["path"]): item["id"] for item in res.json()}
    return ret


def sync_db(path_fs: Set[Path], path_db: Mapping[Path, int]):
    path_db_set = set(path_db)
    to_post = path_fs - path_db_set
    to_delete = path_db_set - path_fs

    print(f"{len(to_post)} to post")
    for path in to_post:
        sess.post(url, json=read_music(path))
        print(f"posted {path}")

    print(f"{len(to_delete)} to delete")
    for path in to_delete:
        if path.exists():
            continue
        sess.delete(f"{url}{path_db[path]}")
        print(f"deleted {path}")


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
