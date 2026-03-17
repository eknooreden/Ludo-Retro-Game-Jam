#!/bin/bash

# ./push_replace.sh https://github.com/eknooreden/Ludo-Retro-Game-Jam.git
# ./push_replace.sh https://github.com/eknooreden/Ludo-Retro-Game-Jam.git "Updated gameplay"

set -e

REPO_URL="$1"
COMMIT_MSG="${2:-New Version}"

if [ -z "$REPO_URL" ]; then
  echo "Usage: ./push_replace.sh <repo-url> [commit-message]"
  exit 1
fi

if [ ! -d ".git" ]; then
  echo "Initializing repo..."
  git init
else
  echo "Git repo already exists. Using existing repo..."
fi

echo "Turning off sparse checkout if enabled..."
git sparse-checkout disable 2>/dev/null || true
git config core.sparseCheckout false || true

echo "Removing old origin if exists..."
git remote remove origin 2>/dev/null || true

echo "Adding origin..."
git remote add origin "$REPO_URL"

echo "Adding files..."
git add -A

if git diff --cached --quiet; then
  echo "No staged changes to commit."
else
  echo "Committing..."
  git commit -m "$COMMIT_MSG"
fi

echo "Setting main branch..."
git branch -M main

echo "Force pushing to GitHub..."
git push -u -f origin main

echo "Done 🚀 Repo replaced."