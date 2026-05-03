# Gen-bot

A multi-tool Telegram bot with AI image generation, AI chatbot, phone number lookup, weather, QR code generator, calculator, and translation — plus a Phone Tracker API deployable on Vercel.

## Features

- **AI Image Generation** (`/img`) — Send a text description and receive an AI-generated image.
- **Phone Number Info** (`/phone`) — Look up carrier, region, timezone, and number type for any phone number.
- **AI Chatbot** (`/chat`) — Chat with an AI directly in Telegram.
- **Weather** (`/weather`) — Get current weather for any city.
- **QR Code Generator** (`/qr`) — Generate QR codes from text or URLs.
- **Calculator** (`/calc`) — Evaluate math expressions safely.
- **Translation** (`/tr`) — Translate text to any language.
- **Phone Tracker API** (`app.py`) — Flask API to look up phone number details. Deployable on Vercel.
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
| `/img <prompt>` | Generate an AI image from a text prompt |
| `/phone <number>` | Phone number info (carrier, region, timezone, type) |
| `/chat <message>` | Chat with an AI |
| `/weather <city>` | Current weather for a city |
| `/qr <text>` | Generate a QR code |
| `/calc <expr>` | Evaluate a math expression |
| `/tr <lang> <text>` | Translate text (e.g. `/tr hi Hello`) |
| *(any text)* | Also generates an image |
| `/stats` | Show bot statistics (admin only) |
| `/broadcast <msg>` | Broadcast a message (admin only, coming soon) |

### Translation Language Codes

| Code | Language |
|------|----------|
| `hi` | Hindi |
| `es` | Spanish |
| `fr` | French |
| `de` | German |
| `ja` | Japanese |
| `zh` | Chinese |
| `ar` | Arabic |
| `ru` | Russian |
| `pt` | Portuguese |
| `ko` | Korean |

## Project Structure

```
Gen-bot/
  app.py           # Phone Tracker API (Vercel entry point)
  bot.py           # Telegram bot entry point
  chatbot.py       # AI chatbot helper for Telegram
  calculator.py    # Safe math expression evaluator
  gen.py           # Image generation Flask API
  gpt.py           # Console AI chatbot
  image_gen.py     # Shared image generation logic
  phone_info.py    # Phone number lookup (phonenumbers library)
  qr_gen.py        # QR code generator
  translator.py    # Text translation (MyMemory API)
  weather.py       # Weather lookup (wttr.in)
  vercel.json      # Vercel deployment config
  requirements.txt
  .gitignore
  README.md
```
