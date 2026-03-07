# ./push_replace.sh https://github.com/eknooreden/Ludo-Retro-Game-Jam.git

REPO_URL=$1
COMMIT_MSG=${2:-"Auto replace repo"}

echo "Initializing repo..."

git init

echo "Removing old origin if exists..."
git remote remove origin 2>/dev/null

echo "Adding origin..."
git remote add origin $REPO_URL

echo "Adding files..."
git add .

echo "Committing..."
git commit -m "$COMMIT_MSG"

echo "Setting main branch..."
git branch -M main

echo "Force pushing to GitHub..."
git push -f origin main

echo "Done; Repo replaced."