# Game Jam Repo Sync Scripts

This guide explains how to use the helper scripts to update specific parts of the project from the GitHub repository.

These scripts allow you to pull only certain folders instead of replacing the entire project.

---

# Scripts Included

| Script | Purpose |
|------|------|
| `only_rpgEngine.sh` | Updates the `rpgEngine` and `assets` folders |
| `only_LudoBoardSystem.sh` | Updates the `LudoBoardSystem` and `assets` folders |
| `push_replace.sh` | Force-pushes the entire project to match your local folder |

---

# Important First Step

Before running any `.sh` script, you must give it permission to run.

Run this command **once per script**:

```bash
chmod +x <script_name>.sh
```

Example:

```bash
chmod +x only_rpgEngine.sh
chmod +x only_LudoBoardSystem.sh
chmod +x push_replace.sh
```

This allows your system to execute the script.

Without this step you may see:

```
zsh: permission denied
```

---

# How to Run the Scripts

All scripts require the GitHub repository URL.

Example repository:

```
https://github.com/eknooreden/Ludo-Retro-Game-Jam.git
```

---

# Updating the RPG Engine

To update the `rpgEngine` and `assets` folders:

```bash
./only_rpgEngine.sh https://github.com/eknooreden/Ludo-Retro-Game-Jam.git
```

This script will:

- clone the repo temporarily
- copy `rpgEngine`
- copy `assets`
- leave the rest of your project unchanged

---

# Updating the Ludo Board System

To update the `LudoBoardSystem` and `assets` folders:

```bash
./only_LudoBoardSystem.sh https://github.com/eknooreden/Ludo-Retro-Game-Jam.git
```

This script will:

- clone the repo temporarily
- copy `LudoBoardSystem`
- copy `assets`
- leave the rest of your project untouched

---

# Replacing the Entire Repository (Advanced)

The `push_replace.sh` script replaces the remote GitHub repository with your current local project.

Use this **only if you want GitHub to exactly match your local files.**

Example:

```bash
./push_replace.sh https://github.com/eknooreden/Ludo-Retro-Game-Jam.git
```

This will:

- initialize Git if needed
- connect to the repository
- push your entire project to GitHub

---

# Safety Notes

These scripts are designed to avoid deleting unrelated project files.

However:

- files with the same name **may be overwritten**
- always commit important work before running scripts

Recommended workflow:

```bash
git add .
git commit -m "Backup before sync"
```

---

# Typical Workflow During the Game Jam

Example workflow for teammates:

1. Pull latest engine updates

```bash
./only_rpgEngine.sh <repo-url>
```

2. Pull latest board system updates

```bash
./only_LudoBoardSystem.sh <repo-url>
```

3. Push completed changes

```bash
./push_replace.sh <repo-url>
```

---

# Troubleshooting

### Permission Denied

Run:

```bash
chmod +x <script_name>.sh
```

### Script Not Found

Make sure you are in the correct folder:

```bash
ls
```

You should see the `.sh` files listed.

---

# Project Structure Example

```
Ludo-Retro-Game-Jam
│
├── assets
├── rpgEngine
├── LudoBoardSystem
│
├── only_rpgEngine.sh
├── only_LudoBoardSystem.sh
├── push_replace.sh
```

---

# Tip

If something goes wrong, always check:

```bash
git status
```

before running scripts again.