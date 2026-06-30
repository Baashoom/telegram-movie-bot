import logging
import os
from telegram.ext import Application, MessageHandler, filters, CommandHandler
from config import BOT_TOKEN
from handlers.group import handle_group_message
from handlers.private import handle_private_message

# Configure logging (force=True overrides any pre-existing handlers)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    force=True,
)
logger = logging.getLogger(__name__)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)


async def start(update, context):
    """Send a message when the command /start is issued."""
    await update.message.reply_text(
        "Hi! I'm a Movie Search Bot. Send me a movie or series name, and I'll find information about it.\n\n"
        "In groups, mention me with @username followed by the movie name.\n\n"
        "Examples:\n"
        "- Inception\n"
        "- Inception 2010\n"
        "- The Dark Knight"
    )


async def help_command(update, context):
    """Send a message when the command /help is issued."""
    await update.message.reply_text(
        "How to use this bot:\n\n"
        "1. Send me a movie or series name\n"
        "2. I'll search for it and provide details\n"
        "3. Click 'Watch Trailer' to see the official trailer\n\n"
        "You can include the year in your search (e.g., 'Inception 2010')\n\n"
        "In groups, mention me with @username followed by the movie name."
    )


def main():
    """Start the bot."""
    if not BOT_TOKEN:
        print("ERROR: BOT_TOKEN is not set!")
        return

    print("Starting bot...")

    application = (
        Application.builder()
        .token(BOT_TOKEN)
        .connect_timeout(30)
        .read_timeout(30)
        .write_timeout(30)
        .build()
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    application.add_handler(
        MessageHandler(filters.ChatType.PRIVATE & filters.TEXT & ~filters.COMMAND, handle_private_message)
    )
    application.add_handler(
        MessageHandler(filters.ChatType.GROUPS & filters.TEXT & ~filters.COMMAND, handle_group_message)
    )

    port = int(os.environ.get("PORT", 8443))
    railway_domain = os.environ.get("RAILWAY_PUBLIC_DOMAIN")

    if railway_domain:
        webhook_url = f"https://{railway_domain}"
        print(f"Using webhook: {webhook_url}")
        application.run_webhook(
            listen="0.0.0.0",
            port=port,
            url_path=BOT_TOKEN,
            webhook_url=webhook_url,
        )
    else:
        print("Using polling mode (local development)")
        application.run_polling(
            allowed_updates=["message"],
            drop_pending_updates=True,
        )


if __name__ == "__main__":
    main()
