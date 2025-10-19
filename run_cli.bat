@echo off
echo Starting MediaImmagine Web Ranking Tool - Command Line Interface
echo.
if "%1"=="" (
    echo Usage: run_cli.bat domain1.com domain2.com [domain3.com]
    echo Example: run_cli.bat google.com facebook.com
    pause
    exit /b 1
)
.\venv\Scripts\python.exe run_tool.py --mode cli --domains %*
pause
