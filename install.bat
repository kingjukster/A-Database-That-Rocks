@echo off
:: Enable UTF-8 encoding for consistent output
chcp 65001 >nul

:: Check if pip is available
python -m pip --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Pip is not installed or not in PATH. Ensure Python and pip are installed.
    pause
    exit /b 1
)

:: Upgrade pip first
echo Upgrading pip...
python -m pip install --upgrade pip

:: Install required packages
echo Installing mysql-connector-python...
pip install mysql-connector-python

echo Installing tk...
pip install tk

echo Installing pillow...
pip install pillow

echo Installing beautifulsoup4...
pip install beautifulsoup4

echo Installing requests...
pip install requests

echo Installation complete.
pause
