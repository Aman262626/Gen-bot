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

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Welcome to Gen-bot!\n\n"
        "Send me a text description and I will generate an AI image for you.\n\n"
        "Commands:\n"
        "/start - Show this welcome message\n"
        "/help - Show help\n"
        "/img <prompt> - Generate an image from a text prompt"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Usage:\n"
        "  /img a sunset over mountains\n"
        "  or just send any text message to generate an image.\n\n"
        "The bot uses an AI image generator to create images from your descriptions."
    )


async def img_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    prompt = " ".join(context.args) if context.args else ""
    if not prompt:
        await update.message.reply_text("Please provide a prompt. Example: /img a cat in space")
        return
    await _generate_and_send(update, prompt)


async def text_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    prompt = update.message.text.strip()
    if not prompt:
        return
    await _generate_and_send(update, prompt)


async def _generate_and_send(update: Update, prompt: str) -> None:
    await update.message.reply_text(f"Generating image for: {prompt}\nPlease wait...")

    try:
        result = generate_image(prompt)
    except Exception as exc:
        logger.error("Image generation failed: %s", exc)
        await update.message.reply_text("Sorry, image generation failed. Please try again later.")
        return

    if result.get("success") and result.get("image_url"):
        await update.message.reply_photo(
            photo=result["image_url"],
            caption=prompt,
        )
    else:
        await update.message.reply_text("Could not generate an image. Please try a different prompt.")


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error("Update %s caused error: %s", update, context.error)


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
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_message))
    app.add_error_handler(error_handler)

    logger.info("Bot started. Polling for updates...")
    app.run_polling()


if __name__ == "__main__":
    main()
