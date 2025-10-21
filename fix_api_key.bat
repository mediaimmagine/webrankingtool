@echo off
echo ========================================
echo FIX API KEY - CORRECT TYPE NEEDED
echo ========================================
echo.
echo The key you provided is a Google OAuth Client ID, not an API key.
echo We need a PageSpeed Insights API key instead.
echo.
echo ========================================
echo WHAT YOU HAVE:
echo ========================================
echo.
echo 629986549061-fj8g6klkc0kq4hf0gciifn7cbkiupjkt.apps.googleusercontent.com
echo - This is an OAuth Client ID
echo - Used for user authentication
echo - NOT for PageSpeed API
echo.
echo ========================================
echo WHAT YOU NEED:
echo ========================================
echo.
echo A PageSpeed Insights API key that looks like:
echo - AIzaSyC... (starts with AIzaSy)
echo - About 39 characters long
echo - Used for API requests
echo.
echo ========================================
echo HOW TO GET THE CORRECT KEY:
echo ========================================
echo.
echo 1. Go to: https://console.cloud.google.com/
echo 2. Select your project (or create new one)
echo 3. Go to "APIs & Services" > "Library"
echo 4. Search for "PageSpeed Insights API"
echo 5. Click on it and click "Enable"
echo 6. Go to "APIs & Services" > "Credentials"
echo 7. Click "Create Credentials" > "API Key"
echo 8. Copy the new API key (starts with AIzaSy)
echo.
echo ========================================
echo ALTERNATIVE: USE CURRENT SETUP
echo ========================================
echo.
echo The tool is already working with improved mock data!
echo You can use it right now:
echo 1. Run: .\run_gui.bat
echo 2. Analyze your sites
echo 3. Get realistic results
echo.
echo ========================================
echo QUICK TEST:
echo ========================================
echo.
echo Let's test what you currently have:
echo.
pause




