import requests
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}


def search_imdb(query: str, year: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    Search IMDb using the suggestion API (stable JSON endpoint).
    Returns basic info if found, or None.
    """
    try:
        # IMDb suggestion API uses first letter of query
        first_letter = query[0].lower() if query else "a"
        url = f"https://v2.sg.media-imdb.com/suggestion/{first_letter}/{query.replace(' ', '_').lower()}.json"

        logger.info(f"Searching IMDb for: {query}")
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()

        data = response.json()
        results = data.get("d", [])

        if not results:
            logger.info("No results from IMDb suggestion API")
            return None

        # Find best match: prefer TV series, then feature films
        best_match = None
        for item in results:
            item_title = item.get("l", "").lower()
            item_type = item.get("q", "")
            item_year = str(item.get("y", ""))

            # Check if title matches
            if query.lower() not in item_title:
                continue

            # If year specified, check match
            if year and item_year and item_year != year:
                continue

            # Prefer TV series for "Friends"-type queries
            if item_type == "TV series":
                best_match = item
                break
            elif not best_match:
                best_match = item

        if not best_match:
            # Just use first result if nothing better
            best_match = results[0]

        title_id = best_match.get("id", "")
        title = best_match.get("l", "Unknown")
        year_found = str(best_match.get("y", ""))
        media_type = "series" if best_match.get("q") == "TV series" else "film"

        logger.info(f"Found on IMDb: {title} ({year_found}) - {media_type} (ID: {title_id})")

        return {
            "id": title_id,
            "title": title,
            "year": year_found if year_found else None,
            "poster_url": best_match.get("i", {}).get("imageUrl", "") if isinstance(best_match.get("i"), dict) else "",
            "plot": "",
            "rating": 0.0,
            "genres": [],
            "media_type": media_type,
            "source": "imdb",
        }

    except Exception as e:
        logger.error(f"IMDb search error: {e}")
        return None
