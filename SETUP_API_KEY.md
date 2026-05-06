# Setting up your Gemini API key safely

Follow these steps **in order**. The goal: your key lives in one file (`.env`), git never sees it, and you never paste it into a place that transmits it (chat, IDE pane, screenshot, Slack, etc.).

If you make a mistake at any step, **stop and ask** — a leaked key is recoverable (delete it, make a new one), but only if you catch it.

---

## 1. Add the `.gitignore` first

Before creating any `.env` file, create `.gitignore` in your project root. The order matters: if you create `.env` *before* `.gitignore` excludes it, a stray `git add .` could stage and commit it.

In your terminal, from the project root:

```
nano .gitignore
```

(Or use any editor — `code .gitignore`, `vim .gitignore`, etc.) Paste in:

```
# Secrets — never commit
.env
.env.*
!.env.example

# Python
__pycache__/
*.py[cod]
*.egg-info/
.venv/
venv/

# OS / editor
.DS_Store
.vscode/
.idea/
```

Save and close. The `.env` lines are the critical ones — they tell git to ignore any file named `.env` (your real key) but still allow `.env.example` (a safe template) if you ever add one.

## 2. Get a key from Google AI Studio

- Open **https://aistudio.google.com/apikey** in a regular browser tab — *not* through an editor pane that has an AI assistant attached.
- Sign in with your Google account, click **Create API key**, and copy the key to your clipboard.

## 3. Create the `.env` file from the **terminal**, not the IDE pane

This is the step where it's easiest to accidentally leak the key. Two rules:

- **Do not paste the key into a chat with an AI assistant** (Claude Code, Copilot Chat, ChatGPT, etc.). Anything you type into those panes is sent over the network.
- **Do not open `.env` in an IDE pane that has an AI assistant attached.** Some assistants send the contents of open files to the model as context.

Open a **terminal** (in VS Code: `Terminal → New Terminal`, or `` Ctrl+` ``). In the terminal, run:

```
printf 'GEMINI_API_KEY=YOUR_KEY_HERE\n' > .env
```

Replace `YOUR_KEY_HERE` with your actual key. Press Enter.

## 4. Lock down file permissions

Make `.env` readable only by your user:

```
chmod 600 .env
```

This isn't strictly required on a personal machine, but it's good hygiene — secrets should not be world-readable.

## 5. Verify git is ignoring `.env`

In the terminal:

```
git status
```

`.env` should **not** appear in the output. If it does, stop — your `.gitignore` isn't catching it. Don't commit anything until you fix that.

You can also explicitly check:

```
git check-ignore -v .env
```

That should print a line pointing to the `.gitignore` rule that's matching. If it prints nothing, the file is *not* ignored.

## 6. Read the key from Python

In `main.py`:

```python
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ["GEMINI_API_KEY"]
```

`load_dotenv()` reads `.env` and adds its variables to the process environment. **Never hardcode the key string in `main.py`** — that defeats every step above.

---

## If you leak your key

It happens. The fix:

1. Go back to **https://aistudio.google.com/apikey** and **delete** the leaked key. (Deleting and revoking are the same thing in AI Studio — the key is invalidated immediately.)
2. Create a new key.
3. Repeat steps 3–5 above with the new key.

**Do not** try to "git rm" a leaked key out of history and call it fixed — once a key has been pushed, scraped, or pasted into a chat, assume it's compromised. Public keys on GitHub get scraped within minutes.

## Common mistakes

- **Pasting the key into the AI chat instead of the terminal.** They look similar in some IDEs. Double-check which pane you're in before pasting a secret.
- **Opening `.env` in an editor with an AI assistant attached.** The file's contents may be sent to the model as context.
- **Committing `.env` because `.gitignore` was added later.** Always set up `.gitignore` first.
- **Hardcoding the key in `main.py` "just for testing."** That file *will* end up in git eventually, with the key still in it.
