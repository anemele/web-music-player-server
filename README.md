# Web Music Player

## Usage

Start the server ...

```bash
uv sync
uv run daphne web_music_player:asgi:application
```

After running the server, sync music data ...

```bash
uv run scripts/sync_db.py <path/to/music>
```
