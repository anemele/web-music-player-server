import json
from itertools import chain, starmap
from pathlib import Path
from turtle import title

from tinytag import TinyTag


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

    return dict(
        id=id,
        path=str(path),
        duration=convert_duration(round(tag['duration'])),
        title=tag.get('title', path.name),
        artist=tag['artist'],
        album=tag['album'],
    )


_STORE = Path('music.json')
if _STORE.exists():
    ITEMS = json.loads(_STORE.read_bytes())
else:
    _MUSIC_LIST = find_music(Path('D:/Music'), *'*.mp3,*.flac'.split(','))
    ITEMS = list(starmap(get_item, enumerate(_MUSIC_LIST)))

    with open(_STORE, 'w', encoding='utf-8') as fp:
        json.dump(ITEMS, fp, ensure_ascii=False)
LENGTH = len(ITEMS)
