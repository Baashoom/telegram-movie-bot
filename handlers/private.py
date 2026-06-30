import logging
from typing import Optional
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from services.search import search_movie, parse_search_query
from utils.formatters import format_movie_message, format_not_found_message

logger = logging.getLogger(__name__)


async def handle_private_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle messages in private chat.
    """
    message = update.message
    if not message or not message.text:
        return

    query = message.text.strip()
    if not query:
        await message.reply_text("Please provide a movie or series name to search.")
        return

    # Parse query
    title, year = parse_search_query(query)

    # Show searching indicator
    searching_message = await message.reply_text("🔍 Searching...")

    # Search for movie
    try:
        movie = search_movie(title, year)

        # Delete searching message
        try:
            await searching_message.delete()
        except Exception:
            pass

        if movie:
            # Format message
            text = format_movie_message(movie)

            # Create poster and message
            if movie.poster_url:
                # Send poster with caption
                try:
                    await context.bot.send_photo(
                        chat_id=message.chat_id,
                        photo=movie.poster_url,
                        caption=text,
                        reply_to_message_id=message.message_id,
                        reply_markup=create_trailer_button(movie.trailer_url),
                    )
                except Exception as e:
                    logger.error(f"Error sending photo: {e}")
                    # Fallback to text-only message
                    await message.reply_text(
                        text,
                        reply_to_message_id=message.message_id,
                        reply_markup=create_trailer_button(movie.trailer_url),
                    )
            else:
                # Text-only message
                await message.reply_text(
                    text,
                    reply_to_message_id=message.message_id,
                    reply_markup=create_trailer_button(movie.trailer_url),
                )
        else:
            # Not found
            await message.reply_text(
                format_not_found_message(title),
                reply_to_message_id=message.message_id,
            )

    except Exception as e:
        logger.error(f"Error searching movie: {e}")
        try:
            await searching_message.delete()
        except Exception:
            pass
        await message.reply_text(
            "An error occurred while searching. Please try again.",
            reply_to_message_id=message.message_id,
        )


def create_trailer_button(trailer_url: str) -> Optional[InlineKeyboardMarkup]:
    """
    Create inline keyboard with "Watch Trailer" button.
    """
    if not trailer_url:
        return None

    keyboard = [[InlineKeyboardButton("Watch Trailer", url=trailer_url)]]
    return InlineKeyboardMarkup(keyboard)
