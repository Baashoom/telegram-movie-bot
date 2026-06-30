import requests
from bs4 import BeautifulSoup
from typing import Optional, Dict, Any
import re
import logging

logger = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}


def search_imdb(query: str, year: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    Search IMDb for a movie or series.
    Returns the first match with details, or None if not found.
    """
    try:
        search_url = f"https://www.imdb.com/find"
        params = {"q": query, "s": "tt", "ttype": "ft,tv"}

        response = requests.get(search_url, params=params, headers=HEADERS, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Find search results
        results = soup.find("div", {"class": "findList"})
        if not results:
            return None

        # Get first result
        first_result = results.find("tr", {"class": "findResultOdd"})
        if not first_result:
            return None

        # Extract title link and ID
        title_link = first_result.find("td", {"class": "result_text"}).find("a")
        if not title_link:
            return None

        title_id = title_link.get("href", "").split("/")[2]
        title_text = title_link.get_text(strip=True)

        # Extract year if available
        year_text = first_result.find("td", {"class": "result_text"}).get_text()
        year_match = re.search(r"\((\d{4})\)", year_text)
        found_year = year_match.group(1) if year_match else None

        # If year is specified, check if it matches
        if year and found_year and year != found_year:
            logger.info(f"Year mismatch: expected {year}, found {found_year}")
            # Continue anyway but note the mismatch

        # Get movie details
        return get_movie_details(title_id)

    except Exception as e:
        logger.error(f"IMDb search error: {e}")
        return None


def get_movie_details(title_id: str) -> Optional[Dict[str, Any]]:
    """
    Get detailed information for a specific IMDb title.
    """
    try:
        url = f"https://www.imdb.com/title/{title_id}/"
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Extract title
        title_tag = soup.find("h1")
        title = title_tag.get_text(strip=True) if title_tag else "Unknown"

        # Extract year
        year_tag = soup.find("span", {"class": "sc-8c396aa2-2"})
        year = year_tag.get_text(strip=True).strip("()") if year_tag else None

        # Extract poster
        poster_tag = soup.find("img", {"class": "ipc-image"})
        poster_url = poster_tag.get("src") if poster_tag else ""

        # Extract plot
        plot_tag = soup.find("span", {"class": "sc-16ede01-2"})
        plot = plot_tag.get_text(strip=True) if plot_tag else ""

        # Extract rating
        rating_tag = soup.find("span", {"class": "sc-bde20123-1"})
        rating = float(rating_tag.get_text(strip=True)) if rating_tag else 0.0

        # Extract genres
        genres = []
        genre_section = soup.find_all("span", {"class": "ipc-chip__text"})
        for genre in genre_section:
            genre_text = genre.get_text(strip=True)
            if genre_text and genre_text not in ["Back to top"]:
                genres.append(genre_text)

        # Determine media type
        media_type = "series" if "/tv/" in url or "TV Series" in str(soup) else "film"

        return {
            "id": title_id,
            "title": title,
            "year": year,
            "poster_url": poster_url,
            "plot": plot,
            "rating": rating,
            "genres": genres[:5],  # Limit to 5 genres
            "media_type": media_type,
            "source": "imdb",
        }

    except Exception as e:
        logger.error(f"IMDb details error: {e}")
        return None
