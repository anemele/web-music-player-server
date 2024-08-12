import json
import time
from dataclasses import asdict, dataclass
from itertools import chain, starmap
from pathlib import Path
from typing import Iterable, List

from dataclass_binder import Binder
from tinytag import TinyTag

from .cache import CACHE_PATH


def convert_duration(s: int) -> str:
    m, s = divmod(s, 60)
    if m < 60:
        return f'{m}:{s:02d}'
    h, m = divmod(m, 60)
    return f'{h}:{m:02d}:{s:02d}'


@dataclass
class MusicItem:
    id: int
    path: str
    duration: str
    title: str
    artist: str
    album: str


@dataclass
class MusicData:
    music: List[MusicItem]
    expire: float


def get_item(id: int, path: Path) -> MusicItem:
    tag = TinyTag.get(path)
    return MusicItem(
        id=id,
        path=str(path),
        duration=convert_duration(round(tag.duration)),  # type: ignore
        title=tag.title or path.name,
        artist=tag.artist or '',
        album=tag.album or '',
    )


def find_music(root: Path, patterns: Iterable[str]):
    return (
        music
        for music in chain.from_iterable(map(root.glob, patterns))
        if music.is_file()
    )


_STORE = CACHE_PATH.joinpath('music.json')
_EXPIRE_TIME = 60 * 60 * 24 * 7
_MUSIC_PATH = Path('D:/Music')
_MUSIC_PATTERN = '*.mp3,*.flac'.split(',')

_flag = True
if _STORE.exists():
    data = Binder(MusicData).bind(json.loads(_STORE.read_bytes()))
    if data.expire > time.time():
        ITEMS = data.music
        _flag = False

if _flag:
    music_path_list = find_music(_MUSIC_PATH, _MUSIC_PATTERN)
    ITEMS = list(starmap(get_item, enumerate(music_path_list)))

    with open(_STORE, 'w', encoding='utf-8') as fp:
        json.dump(
            asdict(MusicData(music=ITEMS, expire=time.time() + _EXPIRE_TIME)),
            fp,
            ensure_ascii=False,
        )


LENGTH = len(ITEMS)
