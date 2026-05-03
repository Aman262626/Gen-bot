# Gen-bot

A Telegram bot and Flask API that generates AI images from text prompts.

## Features

- **Telegram Bot** (`bot.py`) — Send a text description and receive an AI-generated image.
- **Flask API** (`gen.py`) — HTTP endpoint for image generation.
- **Shared image generation module** (`image_gen.py`) — Reusable logic used by both the bot and the API.
- **Admin controls** — Admin-only commands for bot statistics and management.

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Get a Telegram Bot Token

1. Open Telegram and message [@BotFather](https://t.me/BotFather).
2. Send `/newbot` and follow the prompts.
3. Copy the token you receive.

### 3. Set environment variables

```bash
export TELEGRAM_BOT_TOKEN="your-token-here"
export TELEGRAM_ADMIN_ID="your-telegram-user-id"
```

### 4. Run the Telegram bot

```bash
python bot.py
```

The bot will start polling for messages. Send it a text prompt (or use `/img <prompt>`) and it will reply with a generated image.

### 5. Run the Flask API (optional)

```bash
python gen.py
```

The API listens on `http://0.0.0.0:5000`. Generate an image:

```bash
curl "http://localhost:5000/img?prompt=a+cat+in+space"
```

## Bot Commands

| Command | Description |
|---------|-------------|
| `/start` | Welcome message |
| `/help` | Usage instructions |
| `/img <prompt>` | Generate an image from a text description |
| *(any text)* | Also generates an image |

### Admin Commands

| Command | Description |
|---------|-------------|
| `/stats` | Show bot statistics |
| `/broadcast <msg>` | Broadcast a message (coming soon) |

## Project Structure

```
Gen-bot/
  bot.py          # Telegram bot entry point
  gen.py          # Flask API entry point
  image_gen.py    # Shared image generation logic
  requirements.txt
  .gitignore
  README.md
```
