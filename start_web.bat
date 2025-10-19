@echo off
echo Starting Web Ranking Tool Web Interface...
cd /d "%~dp0"
venv\Scripts\activate
python run_tool.py --mode web
pause

