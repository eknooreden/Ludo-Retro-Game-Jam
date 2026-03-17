#!/bin/bash

# ./only_rpgEngine.sh https://github.com/eknooreden/Ludo-Retro-Game-Jam.git

set -e

REPO_URL="$1"
BRANCH="main"
TEMP_DIR="/tmp/rpg_pull_temp"
STAMP=$(date +%Y%m%d_%H%M%S)

if [ -z "$REPO_URL" ]; then
  echo "Usage: ./only_rpgEngine.sh <repo-url>"
  exit 1
fi

echo "Removing old temp folder..."
rm -rf "$TEMP_DIR"

echo "Cloning repo to temp folder..."
git clone --depth 1 --branch "$BRANCH" "$REPO_URL" "$TEMP_DIR"

echo "Backing up local folders..."
cp -R "./rpgEngine" "./rpgEngine_backup_$STAMP" 2>/dev/null || true
cp -R "./assets" "./assets_backup_$STAMP" 2>/dev/null || true

echo "Ensuring target folders exist..."
mkdir -p "./rpgEngine"
mkdir -p "./assets"

echo "Merging rpgEngine files..."
cp -R "$TEMP_DIR/rpgEngine/." "./rpgEngine/" 2>/dev/null || true

echo "Merging assets files..."
cp -R "$TEMP_DIR/assets/." "./assets/" 2>/dev/null || true

echo "Cleaning temp folder..."
rm -rf "$TEMP_DIR"

echo "Done 🚀 Merged: rpgEngine + assets"
echo "Backups:"
echo "  rpgEngine_backup_$STAMP"
echo "  assets_backup_$STAMP"