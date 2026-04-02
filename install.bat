@echo off
title Discord Message Archiver - Setup
color 0A

echo.
echo +===============================================================================+
echo ^|                  DISCORD MESSAGE ARCHIVER - SETUP                             ^|
echo +===============================================================================+
echo.

:: ── Check Python ────────────────────────────────────────────────────────────────
python --version >nul 2>&1
if errorlevel 1 (
    color 0C
    echo  [ERROR] Python is not installed or not on PATH.
    echo.
    echo  Please install Python 3.10 or newer from https://www.python.org/downloads/
    echo  Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

for /f "tokens=2 delims= " %%v in ('python --version 2^>^&1') do set PYVER=%%v
echo  [OK] Python %PYVER% found.
echo.

:: ── Install dependencies ────────────────────────────────────────────────────────
echo  Installing dependencies...
echo.
python -m pip install --upgrade pip --quiet
python -m pip install -r requirements.txt

if errorlevel 1 (
    color 0C
    echo.
    echo  [ERROR] Failed to install dependencies.
    echo  Check the error above and try running: pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

echo.
echo  [OK] All dependencies installed successfully.
echo.

:: ── Create .env if missing ──────────────────────────────────────────────────────
if not exist ".env" (
    copy ".env.example" ".env" >nul
    echo  [OK] Created .env from .env.example (you can edit it to change settings).
) else (
    echo  [OK] .env already exists, skipping.
)
echo.

:: ── Create run.bat ───────────────────────────────────────────────────────────────
echo @echo off > run.bat
echo title Discord Message Archiver >> run.bat
echo color 0A >> run.bat
echo python app.py >> run.bat
echo pause >> run.bat

echo  [OK] Created run.bat - double-click it anytime to start the app.
echo.

echo +===============================================================================+
echo ^|  Setup complete! Run the app by double-clicking run.bat                       ^|
echo ^|  Then open: http://localhost:5000                                             ^|
echo +===============================================================================+
echo.
pause
