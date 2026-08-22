@echo off
cd /d "%~dp0"
echo Установка необходимых компонентов...
python -m pip install -r requirements.txt
echo.
echo Запуск сайта...
start "" http://127.0.0.1:5000
python app.py
pause
