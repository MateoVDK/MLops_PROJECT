#!/usr/bin/env bash
set -euo pipefail

if ! command -v docker >/dev/null 2>&1; then
  echo "Docker is not installed or not available in PATH. Install/open Docker Desktop first."
  exit 1
fi

if ! docker compose version >/dev/null 2>&1; then
  echo "Docker Compose v2 is not available. Update Docker Desktop or install the docker compose plugin."
  exit 1
fi

echo "Starting Blackjack RL Advisor..."
echo "Open: http://localhost:8080"
echo "API docs: http://localhost:8000/docs"

docker compose up --build
