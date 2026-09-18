```bat
@echo off
setlocal

title VITO - Veridian IT Orchestrator

echo ==============================================================
echo              VITO - VERIDIAN IT ORCHESTRATOR
echo                    LOCAL DEVELOPMENT
echo ==============================================================
echo.

set "ROOT_DIR=%~dp0"
set "VENV_DIR=%ROOT_DIR%.venv"

:: 1. Check Python Environment
echo [1/3] Checking Python environment...

if not exist "%VENV_DIR%" (
    echo [*] Creating Python 3.11 virtual environment using uv...
    uv venv "%VENV_DIR%" --python 3.11

    echo [*] Installing dependencies...
    uv pip install --python "%VENV_DIR%\Scripts\python.exe" -r "%ROOT_DIR%requirements.txt"
) else (
    echo [OK] Virtual environment found.
)

:: 2. Start FastAPI
echo.
echo [2/3] Starting FastAPI backend...

start "VITO Backend - FastAPI" /D "%ROOT_DIR%" cmd /k ".venv\Scripts\uvicorn.exe main:app --reload --port 8000"

:: 3. Start Streamlit
echo.
echo [3/3] Starting Streamlit frontend...

start "VITO Frontend - Streamlit" /D "%ROOT_DIR%" cmd /k ".venv\Scripts\streamlit.exe run streamlit\app.py"

echo.
echo ==============================================================
echo  VITO services have been started!
echo.
echo  Backend:   http://localhost:8000
echo  API Docs:  http://localhost:8000/docs
echo  Frontend:  http://localhost:8501
echo ==============================================================
echo.
echo Close the two server windows to stop VITO.
echo.

pause
```
