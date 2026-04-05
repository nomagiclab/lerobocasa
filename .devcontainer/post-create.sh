#!/usr/bin/env bash
set -euo pipefail

ROOT="/workspaces/lerobocasa"
DEP_DIR="$ROOT/.dep"
ROBOSUITE_REPO="$DEP_DIR/robosuite"

REFRESH_ASSETS=false

# Load optional environment variables (to support overriding REFRESH_DEPS)
if [[ -f "$ROOT/.env" ]]; then
  source "$ROOT/.env"
fi

mkdir -p "$DEP_DIR"

echo "Refreshing robosuite checkout..."
rm -rf "$ROBOSUITE_REPO"
git clone --depth 1 --progress https://github.com/ARISE-Initiative/robosuite.git "$ROBOSUITE_REPO"

cd "$ROOT"

rm -rf "$ROOT/.venv"

echo "Installing dependencies with uv sync..."
uv sync

echo "Running RoboSuite macros setup..."
printf 'y\n' | uv run python "$ROBOSUITE_REPO/robosuite/scripts/setup_macros.py"

echo "Running RoboCasa macros setup..."
printf 'y\n' | uv run python -m lerobocasa.scripts.setup_macros

if [[ "${REFRESH_ASSETS:-false}" == "true" ]]; then
    echo "Downloading RoboCasa kitchen assets..."
    printf 'y\n' | uv run python -m lerobocasa.scripts.download_kitchen_assets
fi

echo "Devcontainer setup complete"