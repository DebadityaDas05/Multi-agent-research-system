@echo off
setlocal

:: Navigate to script directory
cd /d "%~dp0"

:: Set window title
title ResearchMind - Multi-Agent AI Research Assistant

echo ===============================================================================
echo                ResearchMind - Multi-Agent AI Research Assistant
echo ===============================================================================
echo.

:: 1. Check for .env file
if not exist ".env" (
    echo [WARNING] .env file not found.
    echo [*] Creating template .env file...
    >".env" echo GEMINI_API_KEY=
    >>".env" echo TAVILY_API_KEY=
    >>".env" echo OPENAI_API_KEY=
    echo [!] Please edit the .env file with your API keys if you haven't already.
    echo.
)

:: 2. Check for virtual environment (.venv)
if exist ".venv\Scripts\python.exe" (
    echo [*] Found existing virtual environment: .venv
) else (
    echo [*] Virtual environment not found. Checking for system Python...
    where python >nul 2>&1
    if errorlevel 1 (
        echo [ERROR] Python was not found on your system PATH.
        echo Please install Python 3.10+ and add it to PATH: https://www.python.org/
        echo.
        pause
        exit /b 1
    )

    echo [*] Creating virtual environment: .venv ...
    python -m venv .venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment.
        pause
        exit /b 1
    )

    echo [*] Installing project dependencies from requirements.txt...
    call .venv\Scripts\activate.bat
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERROR] Dependency installation failed.
        pause
        exit /b 1
    )
)

:: 3. Activate virtual environment
echo [*] Activating virtual environment...
call "%~dp0.venv\Scripts\activate.bat"

:: Ensure Streamlit is installed
where streamlit >nul 2>&1
if errorlevel 1 (
    echo [*] Installing missing requirements...
    pip install -r requirements.txt
)

echo.
:: 4. Mode Selection (Default is Web App; CLI available via argument)
if /i "%~1"=="cli" goto RUN_CLI
if /i "%~1"=="pipeline" goto RUN_CLI
if /i "%~1"=="--cli" goto RUN_CLI

:RUN_WEB
echo [*] Starting Streamlit Web Application...
echo [*] Opening in your default browser at http://localhost:8501
echo [*] Press Ctrl+C in this console to stop the server.
echo ===============================================================================
echo.
streamlit run app.py
goto FINISH

:RUN_CLI
echo [*] Starting ResearchMind CLI Pipeline...
echo ===============================================================================
echo.
python pipeline.py
goto FINISH

:FINISH
if errorlevel 1 (
    echo.
    echo [NOTICE] Application process finished with exit code %errorlevel%.
)
echo.
echo Press any key to close this window...
pause >nul
