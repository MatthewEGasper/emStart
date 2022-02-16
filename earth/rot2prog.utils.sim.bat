@echo off
cd /d %~dp0
CALL .venv\Scripts\activate.bat

python -m rot2prog.utils.sim