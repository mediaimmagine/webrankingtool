@echo off
echo Starting MediaImmagine Web Ranking Tool GUI...
cd /d "%~dp0"
venv\Scripts\activate
python gui_app.py
pause
