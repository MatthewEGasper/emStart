@echo off
cd /d %~dp0
CALL .venv\Scripts\activate.bat
cd src
cmd.exe
pause