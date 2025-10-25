@echo off
echo ========================================
echo Building Windows Portable Executable
echo ========================================
echo.

cd /d "%~dp0"

echo Installing required packages...
pip install -r requirements_image_resizer.txt
pip install pyinstaller

echo.
echo Building executable...
pyinstaller --clean build_windows.spec

echo.
echo ========================================
echo Build complete!
echo ========================================
echo.
echo Executable location: dist\ImageResizerCOED.exe
echo.
pause

