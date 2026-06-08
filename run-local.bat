@echo off
setlocal

REM Always use the folder where this .bat file is located as the project root
set "ROOT=%~dp0"

REM Check that the expected folders exist
if not exist "%ROOT%backend\app\main.py" (
    echo Could not find backend\app\main.py
    echo Put this file in the root of MLops_PROJECT and run it again.
    pause
    exit /b 1
)

if not exist "%ROOT%frontend\index.html" (
    echo Could not find frontend\index.html
    echo Put this file in the root of MLops_PROJECT and run it again.
    pause
    exit /b 1
)

REM Check Python
where python >nul 2>nul
if errorlevel 1 (
    echo Python was not found in PATH.
    echo Install Python or enable "Add Python to PATH", then try again.
    pause
    exit /b 1
)

echo Starting backend API on http://127.0.0.1:8000
echo Starting frontend on http://127.0.0.1:5500

REM Backend: equivalent to running this from the backend folder:
REM uvicorn app.main:app --reload
start "Backend API" /D "%ROOT%backend" cmd /k "python -m uvicorn app.main:app --reload"

REM Frontend: equivalent to running this from the frontend folder:
REM python -m http.server 5500
start "Frontend Server" /D "%ROOT%frontend" cmd /k "python -m http.server 5500"

REM Give the servers a moment to start, then open the frontend
timeout /t 2 /nobreak >nul
start "" "http://127.0.0.1:5500"

endlocal
