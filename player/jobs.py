import json
import time
from itertools import chain, starmap
from pathlib import Path
from typing import Iterable

from tinytag import TinyTag


def find_music(root: Path, patterns: Iterable[str]):
    return (
        music
        for music in chain.from_iterable(map(root.glob, patterns))
        if music.is_file()
    )


def convert_duration(s: int) -> str:
    m, s = divmod(s, 60)
    if m < 60:
        return f'{m}:{s:02d}'
    h, m = divmod(m, 60)
    return f'{h}:{m:02d}:{s:02d}'


def get_item(id: int, path: Path):
    tag = TinyTag.get(path).as_dict()

    return dict(
        id=id,
        path=str(path),
        duration=convert_duration(round(tag['duration'])),
        title=tag['title'] or path.name,
        artist=tag['artist'] or '',
        album=tag['album'] or '',
    )


def is_expired(path: Path):
    return float(path.read_text().strip()) < time.time()


_EXPIRE = Path('expire.txt')
_EXPIRE_TIME = 60 * 60 * 24 * 7
_STORE = Path('music.json')

if _EXPIRE.exists() and not is_expired(_EXPIRE) and _STORE.exists():
    ITEMS = json.loads(_STORE.read_bytes())
else:
    _MUSIC_LIST = find_music(Path('D:/Music'), '*.mp3,*.flac'.split(','))
    ITEMS = list(starmap(get_item, enumerate(_MUSIC_LIST)))

    with open(_STORE, 'w', encoding='utf-8') as fp:
        json.dump(ITEMS, fp, ensure_ascii=False)

    _EXPIRE.write_text(str(time.time() + _EXPIRE_TIME))

LENGTH = len(ITEMS)
