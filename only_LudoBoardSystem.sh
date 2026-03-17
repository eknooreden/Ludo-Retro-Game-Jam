#!/bin/bash

# ./only_LudoBoardSystem.sh https://github.com/eknooreden/Ludo-Retro-Game-Jam.git

set -e

REPO_URL="$1"
BRANCH="main"
TEMP_DIR="/tmp/ludo_pull_temp"
STAMP=$(date +%Y%m%d_%H%M%S)

if [ -z "$REPO_URL" ]; then
  echo "Usage: ./only_LudoBoardSystem.sh <repo-url>"
  exit 1
fi

echo "Removing old temp folder..."
rm -rf "$TEMP_DIR"

echo "Cloning repo to temp folder..."
git clone --depth 1 --branch "$BRANCH" "$REPO_URL" "$TEMP_DIR"

echo "Backing up local folders..."
cp -R "./LudoBoardSystem" "./LudoBoardSystem_backup_$STAMP" 2>/dev/null || true
cp -R "./assets" "./assets_backup_$STAMP" 2>/dev/null || true

echo "Ensuring target folders exist..."
mkdir -p "./LudoBoardSystem"
mkdir -p "./assets"

echo "Merging LudoBoardSystem files..."
cp -R "$TEMP_DIR/LudoBoardSystem/." "./LudoBoardSystem/" 2>/dev/null || true

echo "Merging assets files..."
cp -R "$TEMP_DIR/assets/." "./assets/" 2>/dev/null || true

echo "Cleaning temp folder..."
rm -rf "$TEMP_DIR"

echo "Done 🚀 Merged: LudoBoardSystem + assets"
echo "Backups:"
echo "  LudoBoardSystem_backup_$STAMP"
echo "  assets_backup_$STAMP"