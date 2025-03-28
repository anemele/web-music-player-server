import time
from dataclasses import dataclass
from itertools import chain
from pathlib import Path
from typing import Iterable

from mashumaro.mixins.orjson import DataClassORJSONMixin
from mashumaro.mixins.toml import DataClassTOMLMixin
from tinytag import TinyTag


LOCAL_DIR = Path(".local")
LOCAL_DIR.mkdir(exist_ok=True)
if not (gi := LOCAL_DIR / ".gitignore").exists():
    gi.write_text("*")


# 服务器配置清单
@dataclass
class ServerConfig(DataClassTOMLMixin):
    fs_root: Path
    host: str = "localhost"
    port: int = 5000
    debug: bool = True


# 服务器配置文件
SERVER_CONFIG_FILE = LOCAL_DIR / "server.config.toml"


# 服务器配置
def load_server_config():
    return ServerConfig.from_toml(SERVER_CONFIG_FILE.read_text())


# 音乐数据（tag）
@dataclass
class MusicTag(DataClassORJSONMixin):
    title: str
    artist: str
    album: str
    duration: str


# 音乐数据（网络传输）
@dataclass
class MusicItem(MusicTag):
    id: int


# 音乐数据（服务器缓存）
@dataclass
class MusicItemCache(MusicTag):
    path: Path


@dataclass
class MusicDataCache(DataClassORJSONMixin):
    music: list[MusicItemCache]
    expire: float


EXPIRE_TIME = 60 * 60 * 24 * 7
CACHE_FILE = LOCAL_DIR / "music.json"


def convert_duration(s: int) -> str:
    m, s = divmod(s, 60)
    if m < 60:
        return f"{m}:{s:02d}"
    h, m = divmod(m, 60)
    return f"{h}:{m:02d}:{s:02d}"


def get_tag(path: Path) -> MusicTag:
    tag = TinyTag.get(path)
    return MusicTag(
        duration=convert_duration(round(tag.duration or 0.0)),
        title=tag.title or path.name,
        artist=tag.artist or "",
        album=tag.album or "",
    )


def find_music(
    root: Path, patterns: Iterable[str] = ("*.mp3", "*.flac")
) -> Iterable[Path]:
    return (
        music
        for music in chain.from_iterable(map(root.glob, patterns))
        if music.is_file()
    )


EXPORT_TYPE = tuple[list[MusicItem], list[Path], ServerConfig]


def load_data() -> EXPORT_TYPE:
    server_config = load_server_config()
    # 1. 从缓存中加载数据
    if CACHE_FILE.exists():
        data = MusicDataCache.from_json(CACHE_FILE.read_bytes())
        # 2. 判断是否过期
        if data.expire > time.time():
            r0 = []
            r1 = []
            for i, music in enumerate(data.music):
                r1.append(music.path)
                r0.append(MusicItem.from_dict({"id": i, **music.to_dict()}))
            return r0, r1, server_config
    # 3. 缓存不存在或已过期，重新生成数据
    music_path_list = find_music(server_config.fs_root)
    r0 = []
    r1 = []
    cache_data = []
    for i, music in enumerate(music_path_list):
        r1.append(music)
        tag = get_tag(music).to_dict()
        r0.append(MusicItem(id=i, **tag))
        cache_data.append(MusicItemCache(path=music, **tag))

    # 4. 缓存数据
    expire_time = time.time() + EXPIRE_TIME
    cache = MusicDataCache(
        music=cache_data,
        expire=expire_time,
    )
    CACHE_FILE.write_bytes(cache.to_jsonb())

    return r0, r1, server_config
