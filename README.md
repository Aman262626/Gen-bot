# Gen-bot

A multi-tool project featuring a Telegram bot for AI image generation, a chatbot, and a Phone Tracker API deployable on Vercel.

## Features

- **Telegram Bot** (`bot.py`) — Send a text description and receive an AI-generated image.
- **Phone Tracker API** (`app.py`) — Flask API to look up phone number details. Deployable on Vercel.
- **AI Chatbot** (`gpt.py`) — Console-based AI chatbot.
- **Image Generation API** (`gen.py`) — Flask HTTP endpoint for AI image generation.
- **Admin controls** — Admin-only Telegram bot commands for bot statistics.

## Vercel Deployment (Phone Tracker API)

The project is configured for Vercel deployment out of the box.

1. Import the repo at [vercel.com/new](https://vercel.com/new)
2. Vercel auto-detects `vercel.json` and deploys `app.py`
3. Access the API at: `https://your-app.vercel.app/api?number=XXXXXXXXXX`

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API info and usage |
| `/api?number=XXXXXXXXXX` | GET | Trace a phone number |

## Telegram Bot Setup

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

### Bot Commands

| Command | Description |
|---------|-------------|
| `/start` | Welcome message |
| `/help` | Usage instructions |
| `/img <prompt>` | Generate an image from a text description |
| *(any text)* | Also generates an image |
| `/stats` | Show bot statistics (admin only) |
| `/broadcast <msg>` | Broadcast a message (admin only, coming soon) |

## Project Structure

```
Gen-bot/
  app.py           # Phone Tracker API (Vercel entry point)
  bot.py           # Telegram bot entry point
  gen.py           # Image generation Flask API
  gpt.py           # Console AI chatbot
  image_gen.py     # Shared image generation logic
  vercel.json      # Vercel deployment config
  requirements.txt
  .gitignore
  README.md
```
