@echo off
cd /d %~dp0
CALL .venv\Scripts\activate.bat
cd src
python.exe -m earth
pause