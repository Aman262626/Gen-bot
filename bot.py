import os
import logging

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from image_gen import generate_image
from phone_info import lookup_number
from chatbot import get_chat_response
from weather import get_weather
from qr_gen import generate_qr
from calculator import safe_eval
from translator import translate_text

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
ADMIN_ID = int(os.environ.get("TELEGRAM_ADMIN_ID", "0"))


def _is_admin(user_id: int) -> bool:
    return ADMIN_ID != 0 and user_id == ADMIN_ID


# ──────────────────────────── /start & /help ────────────────────────────


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = (
        "Welcome to Gen-bot!\n\n"
        "Commands:\n"
        "/start - Welcome message\n"
        "/help - Show help\n"
        "/img <prompt> - Generate AI image\n"
        "/phone <number> - Phone number info\n"
        "/chat <message> - AI chatbot\n"
        "/weather <city> - Weather info\n"
        "/qr <text> - Generate QR code\n"
        "/calc <expression> - Calculator\n"
        "/tr <lang> <text> - Translate text"
    )
    if _is_admin(update.effective_user.id):
        text += (
            "\n\nAdmin commands:\n"
            "/stats - Bot statistics\n"
            "/broadcast <message> - Broadcast (coming soon)"
        )
    await update.message.reply_text(text)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Usage examples:\n\n"
        "/img a sunset over mountains\n"
        "/phone +919876543210\n"
        "/chat What is AI?\n"
        "/weather Delhi\n"
        "/qr https://example.com\n"
        "/calc 2 + 2 * 3\n"
        "/tr hi Hello, how are you?\n"
        "  (translates to Hindi)\n\n"
        "Or just send any text to generate an image."
    )


# ──────────────────────────── /img ──────────────────────────────────────


async def img_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    prompt = " ".join(context.args) if context.args else ""
    if not prompt:
        await update.message.reply_text(
            "Please provide a prompt. Example: /img a cat in space"
        )
        return
    await _generate_and_send(update, prompt)


async def text_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    prompt = update.message.text.strip()
    if not prompt:
        return
    await _generate_and_send(update, prompt)


async def _generate_and_send(update: Update, prompt: str) -> None:
    await update.message.reply_text(
        f"Generating image for: {prompt}\nPlease wait..."
    )
    try:
        result = generate_image(prompt)
    except Exception as exc:
        logger.error("Image generation failed: %s", exc)
        await update.message.reply_text(
            "Sorry, image generation failed. Please try again later."
        )
        return

    if result.get("success") and result.get("image_url"):
        await update.message.reply_photo(photo=result["image_url"], caption=prompt)
    else:
        await update.message.reply_text(
            "Could not generate an image. Please try a different prompt."
        )


# ──────────────────────────── /phone ────────────────────────────────────


async def phone_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    number = " ".join(context.args) if context.args else ""
    if not number:
        await update.message.reply_text(
            "Please provide a phone number.\n"
            "Example: /phone +919876543210"
        )
        return

    await update.message.reply_text("Looking up number...")
    info = lookup_number(number)

    if "error" in info:
        await update.message.reply_text(f"Error: {info['error']}")
        return

    lines = [
        f"Phone Number Info",
        f"{'─' * 28}",
        f"Number: {info['international']}",
        f"National: {info['national']}",
        f"Valid: Yes",
        f"Type: {info['number_type']}",
        f"Carrier: {info['carrier']}",
        f"Region: {info['region']}",
        f"Country: {info['country']}",
        f"Timezone: {info['timezone']}",
    ]
    await update.message.reply_text("\n".join(lines))


# ──────────────────────────── /chat ─────────────────────────────────────


async def chat_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    question = " ".join(context.args) if context.args else ""
    if not question:
        await update.message.reply_text(
            "Please provide a message.\nExample: /chat What is Python?"
        )
        return

    await update.message.reply_text("Thinking...")
    response = get_chat_response(question)
    await update.message.reply_text(response)


# ──────────────────────────── /weather ──────────────────────────────────


async def weather_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    city = " ".join(context.args) if context.args else ""
    if not city:
        await update.message.reply_text(
            "Please provide a city name.\nExample: /weather Delhi"
        )
        return

    await update.message.reply_text("Fetching weather...")
    info = get_weather(city)

    if "error" in info:
        await update.message.reply_text(f"Error: {info['error']}")
        return

    lines = [
        f"Weather — {info['city']}",
        f"{'─' * 28}",
        f"Condition: {info['description']}",
        f"Temperature: {info['temperature']}",
        f"Feels Like: {info['feels_like']}",
        f"Humidity: {info['humidity']}",
        f"Wind: {info['wind']}",
        f"Visibility: {info['visibility']}",
        f"Pressure: {info['pressure']}",
    ]
    await update.message.reply_text("\n".join(lines))


# ──────────────────────────── /qr ───────────────────────────────────────


async def qr_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = " ".join(context.args) if context.args else ""
    if not text:
        await update.message.reply_text(
            "Please provide text or a URL.\nExample: /qr https://example.com"
        )
        return

    buf = generate_qr(text)
    await update.message.reply_photo(photo=buf, caption=f"QR: {text}")


# ──────────────────────────── /calc ─────────────────────────────────────


async def calc_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    expression = " ".join(context.args) if context.args else ""
    if not expression:
        await update.message.reply_text(
            "Please provide an expression.\nExample: /calc 2 + 2 * 3"
        )
        return

    result = safe_eval(expression)
    await update.message.reply_text(f"{expression} = {result}")


# ──────────────────────────── /tr ───────────────────────────────────────


async def tr_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    args = context.args if context.args else []
    if len(args) < 2:
        await update.message.reply_text(
            "Usage: /tr <lang_code> <text>\n"
            "Example: /tr hi Hello, how are you?\n\n"
            "Common codes: hi (Hindi), es (Spanish), fr (French), "
            "de (German), ja (Japanese), zh (Chinese), ar (Arabic), "
            "ru (Russian), pt (Portuguese), ko (Korean)"
        )
        return

    target_lang = args[0]
    text = " ".join(args[1:])

    await update.message.reply_text("Translating...")
    result = translate_text(text, target_lang=target_lang)

    if "error" in result:
        await update.message.reply_text(f"Error: {result['error']}")
        return

    await update.message.reply_text(
        f"Translation ({result['target_lang']}):\n{result['translated_text']}"
    )


# ──────────────────────────── Admin ─────────────────────────────────────


async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not _is_admin(update.effective_user.id):
        await update.message.reply_text(
            "This command is only available to the bot admin."
        )
        return
    await update.message.reply_text(
        "Bot Statistics:\n"
        f"  Bot is running\n"
        f"  Admin ID: {ADMIN_ID}\n"
        f"  Your ID: {update.effective_user.id}"
    )


async def broadcast_command(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    if not _is_admin(update.effective_user.id):
        await update.message.reply_text(
            "This command is only available to the bot admin."
        )
        return
    await update.message.reply_text("Broadcast feature coming soon!")


# ──────────────────────────── Error ─────────────────────────────────────


async def error_handler(
    update: object, context: ContextTypes.DEFAULT_TYPE
) -> None:
    logger.error("Update %s caused error: %s", update, context.error)


# ──────────────────────────── Main ──────────────────────────────────────


def main() -> None:
    if not BOT_TOKEN:
        raise RuntimeError(
            "TELEGRAM_BOT_TOKEN environment variable is not set. "
            "Get a token from @BotFather on Telegram."
        )

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("img", img_command))
    app.add_handler(CommandHandler("phone", phone_command))
    app.add_handler(CommandHandler("chat", chat_command))
    app.add_handler(CommandHandler("weather", weather_command))
    app.add_handler(CommandHandler("qr", qr_command))
    app.add_handler(CommandHandler("calc", calc_command))
    app.add_handler(CommandHandler("tr", tr_command))
    app.add_handler(CommandHandler("stats", stats_command))
    app.add_handler(CommandHandler("broadcast", broadcast_command))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, text_message)
    )
    app.add_error_handler(error_handler)

    logger.info("Bot started. Polling for updates...")
    app.run_polling()


if __name__ == "__main__":
    main()
