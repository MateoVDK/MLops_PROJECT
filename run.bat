@echo off
where docker >nul 2>nul
if errorlevel 1 (
  echo Docker is not installed or not available in PATH. Install/open Docker Desktop first.
  exit /b 1
)

docker compose version >nul 2>nul
if errorlevel 1 (
  echo Docker Compose v2 is not available. Update Docker Desktop or install the docker compose plugin.
  exit /b 1
)

echo Starting Blackjack RL Advisor...
echo Open: http://localhost:8080
echo API docs: http://localhost:8000/docs

docker compose up --build
