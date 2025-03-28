@echo off

pushd %~dp0
call .venv\Scripts\python.exe -m music_player_server
popd
