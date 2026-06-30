from typing import Optional
from models.movie import MovieResult


def format_movie_message(movie: MovieResult) -> str:
    """
    Format a movie result into a Telegram message.
    """
    # Title with year
    if movie.year:
        title_line = f"{movie.title} ({movie.year})"
    else:
        title_line = movie.title

    # Plot (limit to 2 sentences)
    plot = movie.plot
    if plot:
        # Split by sentence endings and take first 2
        sentences = plot.replace(". ", ".|").split("|")
        plot = ". ".join(sentences[:2])
        if not plot.endswith("."):
            plot += "."

    # Rating (round to 1 decimal place)
    try:
        rating_val = round(float(movie.rating), 1)
        rating_line = f"Rating: {rating_val}/10" if rating_val > 0 else "Rating: N/A"
    except (ValueError, TypeError):
        rating_line = "Rating: N/A"

    # Media type hashtag
    media_type_tag = "#series" if movie.media_type == "series" else "#film"

    # Genre hashtags
    genre_tags = " ".join([f"#{genre}" for genre in movie.genres[:5]])

    # Build message
    message_parts = [title_line, ""]

    if plot:
        message_parts.append(plot)
        message_parts.append("")

    message_parts.append(rating_line)
    message_parts.append("")
    message_parts.append(media_type_tag)

    if genre_tags:
        message_parts.append(genre_tags)

    return "\n".join(message_parts)


def format_not_found_message(title: str) -> str:
    """
    Format a "not found" message.
    """
    return f"Sorry, I couldn't find this movie or series."
