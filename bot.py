import logging
from telegram.ext import Application, MessageHandler, filters, CommandHandler
from config import BOT_TOKEN
from handlers.group import handle_group_message
from handlers.private import handle_private_message

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


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
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # Group message handler (when bot is mentioned)
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_group_message)
    )

    # Private chat handler
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_private_message)
    )

    # Run the bot
    logger.info("Starting bot...")
    application.run_polling(allowed_updates=["message"])


if __name__ == "__main__":
    main()
