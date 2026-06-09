@echo off
setlocal

REM Always use the folder where this .bat file is located as the project root
set "ROOT=%~dp0"

if not exist "%ROOT%docker-compose.yml" (
    echo Could not find docker-compose.yml
    echo Put this file in the root of MLops_PROJECT and run it again.
    pause
    exit /b 1
)

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

where docker >nul 2>nul
if errorlevel 1 (
    echo Docker was not found in PATH.
    echo Install or open Docker Desktop, then run this file again.
    pause
    exit /b 1
)

docker compose version >nul 2>nul
if errorlevel 1 (
    echo Docker Compose v2 was not found.
    echo Update Docker Desktop or install the Docker Compose plugin, then try again.
    pause
    exit /b 1
)

docker info >nul 2>nul
if errorlevel 1 (
    echo Docker is installed, but the Docker engine is not running.
    echo Open Docker Desktop and wait until it has fully started, then run this file again.
    pause
    exit /b 1
)

echo Starting everything needed for Blackjack RL Advisor...
echo Frontend: http://127.0.0.1:8088
echo API docs: http://127.0.0.1:8000/docs
echo Database: postgres container managed by docker compose

start "MLops Docker Compose" /D "%ROOT%" cmd /k "docker compose up --build"

timeout /t 8 /nobreak >nul
start "" "http://127.0.0.1:8088"

endlocal
