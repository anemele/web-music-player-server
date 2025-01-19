from pathlib import Path

CACHE_PATH = Path(".cache")
if not CACHE_PATH.exists():
    CACHE_PATH.mkdir()
    CACHE_PATH.joinpath(".gitignore").write_text("*")
