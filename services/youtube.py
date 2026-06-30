import requests
from typing import Optional
import logging
from config import YOUTUBE_API_KEY, YOUTUBE_BASE_URL

logger = logging.getLogger(__name__)


def search_trailer(title: str, year: Optional[str] = None) -> Optional[str]:
    """
    Search YouTube for an official trailer.
    Returns the video URL or None if not found.
    """
    try:
        # Build search query
        query = f"{title} official trailer"
        if year:
            query += f" {year}"

        params = {
            "part": "snippet",
            "q": query,
            "type": "video",
            "videoCategoryId": "1",  # Film & Animation
            "maxResults": 5,
            "key": YOUTUBE_API_KEY,
        }

        response = requests.get(f"{YOUTUBE_BASE_URL}/search", params=params, timeout=10)
        response.raise_for_status()

        data = response.json()
        if not data.get("items"):
            return None

        # Find the best trailer (prefer official channels)
        for item in data["items"]:
            snippet = item.get("snippet", {})
            title_lower = snippet.get("title", "").lower()

            # Check if it's likely a trailer
            if any(
                keyword in title_lower
                for keyword in ["trailer", "official", "preview", "teaser"]
            ):
                video_id = item.get("id", {}).get("videoId")
                if video_id:
                    return f"https://www.youtube.com/watch?v={video_id}"

        # If no obvious trailer found, return first result
        if data["items"]:
            video_id = data["items"][0].get("id", {}).get("videoId")
            if video_id:
                return f"https://www.youtube.com/watch?v={video_id}"

        return None

    except Exception as e:
        logger.error(f"YouTube search error: {e}")
        return None
