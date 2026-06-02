@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"

if not exist ".venv\Scripts\activate.bat" (
    echo Error: Virtual environment not found. Run:
    echo python -m venv .venv
    echo .venv\Scripts\python.exe -m pip install -r requirements.txt
    pause
    exit /b 1
)

call .venv\Scripts\activate.bat
if !errorlevel! neq 0 (
    echo Error: Failed to activate virtual environment
    pause
    exit /b 1
)

echo Installing/updating dependencies...
pip install -q -r requirements.txt

echo.
echo Starting Streamlit app...
streamlit run app.py
