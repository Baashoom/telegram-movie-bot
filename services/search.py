import re
from typing import Optional, Tuple
import logging
from services.imdb import search_imdb
from services.tmdb import search_tmdb
from models.movie import MovieResult

logger = logging.getLogger(__name__)


def parse_search_query(query: str) -> Tuple[str, Optional[str]]:
    """
    Parse search query to extract title and optional year.
    Returns (title, year) tuple.
    """
    # Remove bot mention if present
    query = re.sub(r"@\w+", "", query).strip()

    # Try to extract year (4 digits at the end or in parentheses)
    year_match = re.search(r"\b(\d{4})\b$", query)
    if year_match:
        year = year_match.group(1)
        title = query[: year_match.start()].strip()
    else:
        # Check for year in parentheses
        year_match = re.search(r"\((\d{4})\)", query)
        if year_match:
            year = year_match.group(1)
            title = re.sub(r"\(\d{4}\)", "", query).strip()
        else:
            year = None
            title = query.strip()

    return title, year


def search_movie(title: str, year: Optional[str] = None) -> Optional[MovieResult]:
    """
    Search for a movie or series across multiple sources.
    Returns a MovieResult or None if not found.
    """
    logger.info(f"Searching for: {title} ({year})")

    # Try TMDB first (reliable API)
    result = search_tmdb(title, year)
    if result:
        logger.info(f"Found on TMDB: {result['title']}")
        return MovieResult(
            title=result["title"],
            year=result.get("year"),
            poster_url=result.get("poster_url", ""),
            plot=result.get("plot", ""),
            rating=result.get("rating", 0.0),
            rating_source="tmdb",
            genres=result.get("genres", []),
            trailer_url=None,
            media_type=result.get("media_type", "film"),
        )

    # Try IMDb as fallback (suggestion API)
    result = search_imdb(title, year)
    if result:
        logger.info(f"Found on IMDb: {result['title']}")
        return MovieResult(
            title=result["title"],
            year=result.get("year"),
            poster_url=result.get("poster_url", ""),
            plot=result.get("plot", ""),
            rating=result.get("rating", 0.0),
            rating_source="imdb",
            genres=result.get("genres", []),
            trailer_url=None,
            media_type=result.get("media_type", "film"),
        )

    logger.info(f"Not found: {title}")
    return None
