import requests
from typing import Optional, Dict, Any, List
import logging
from config import TMDB_API_KEY, TMDB_BASE_URL, TMDB_POSTER_SIZE

logger = logging.getLogger(__name__)


def search_tmdb(query: str, year: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    Search TMDB for a movie or TV series.
    Returns the best match, preferring TV series when both exist.
    """
    try:
        logger.info(f"Searching TMDB for: {query}")

        movie_result = search_tmdb_movies(query, year)
        tv_result = search_tmdb_tv(query, year)

        if movie_result and tv_result:
            # Prefer TV series — most user queries for show names want the series
            logger.info(f"Preferring TV result: {tv_result['title']}")
            return tv_result
        elif tv_result:
            logger.info(f"Found TV series: {tv_result['title']}")
            return tv_result
        elif movie_result:
            logger.info(f"Found movie: {movie_result['title']}")
            return movie_result

        logger.info(f"Not found on TMDB: {query}")
        return None

    except Exception as e:
        logger.error(f"TMDB search error: {e}")
        return None


def search_tmdb_movies(query: str, year: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    Search TMDB for movies.
    """
    try:
        logger.info(f"Searching TMDB movies for: {query}")
        params = {
            "api_key": TMDB_API_KEY,
            "query": query,
            "language": "en-US",
            "include_adult": "false",
        }
        if year:
            params["year"] = year

        logger.info(f"TMDB API key: {TMDB_API_KEY[:8]}..." if TMDB_API_KEY else "No API key")
        response = requests.get(f"{TMDB_BASE_URL}/search/movie", params=params, timeout=10)
        logger.info(f"TMDB response status: {response.status_code}")
        response.raise_for_status()

        data = response.json()
        logger.info(f"TMDB results count: {len(data.get('results', []))}")

        if not data.get("results"):
            return None

        # Get first result
        first_movie = data["results"][0]
        movie_id = first_movie["id"]
        logger.info(f"Found movie: {first_movie.get('title')} (ID: {movie_id})")

        # Get detailed information
        return get_movie_details(movie_id)

    except Exception as e:
        logger.error(f"TMDB movie search error: {e}")
        return None


def search_tmdb_tv(query: str, year: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    Search TMDB for TV series.
    """
    try:
        params = {
            "api_key": TMDB_API_KEY,
            "query": query,
            "language": "en-US",
            "include_adult": "false",
        }
        if year:
            params["first_air_date_year"] = year

        response = requests.get(f"{TMDB_BASE_URL}/search/tv", params=params, timeout=10)
        response.raise_for_status()

        data = response.json()
        if not data.get("results"):
            return None

        # Get first result
        first_show = data["results"][0]
        show_id = first_show["id"]

        # Get detailed information
        return get_tv_details(show_id)

    except Exception as e:
        logger.error(f"TMDB TV search error: {e}")
        return None


def get_movie_details(movie_id: int) -> Optional[Dict[str, Any]]:
    """
    Get detailed information for a specific movie.
    """
    try:
        params = {"api_key": TMDB_API_KEY, "language": "en-US"}

        response = requests.get(f"{TMDB_BASE_URL}/movie/{movie_id}", params=params, timeout=10)
        response.raise_for_status()

        movie = response.json()

        # Extract poster
        poster_path = movie.get("poster_path", "")
        poster_url = f"https://image.tmdb.org/t/p/{TMDB_POSTER_SIZE}{poster_path}" if poster_path else ""

        # Extract genres
        genres = [genre["name"] for genre in movie.get("genres", [])]

        return {
            "id": movie_id,
            "title": movie.get("title", "Unknown"),
            "year": movie.get("release_date", "")[:4] if movie.get("release_date") else None,
            "poster_url": poster_url,
            "plot": movie.get("overview", ""),
            "rating": movie.get("vote_average", 0.0),
            "genres": genres,
            "media_type": "film",
            "source": "tmdb",
        }

    except Exception as e:
        logger.error(f"TMDB movie details error: {e}")
        return None


def get_tv_details(show_id: int) -> Optional[Dict[str, Any]]:
    """
    Get detailed information for a specific TV series.
    """
    try:
        params = {"api_key": TMDB_API_KEY, "language": "en-US"}

        response = requests.get(f"{TMDB_BASE_URL}/tv/{show_id}", params=params, timeout=10)
        response.raise_for_status()

        show = response.json()

        # Extract poster
        poster_path = show.get("poster_path", "")
        poster_url = f"https://image.tmdb.org/t/p/{TMDB_POSTER_SIZE}{poster_path}" if poster_path else ""

        # Extract genres
        genres = [genre["name"] for genre in show.get("genres", [])]

        return {
            "id": show_id,
            "title": show.get("name", "Unknown"),
            "year": show.get("first_air_date", "")[:4] if show.get("first_air_date") else None,
            "poster_url": poster_url,
            "plot": show.get("overview", ""),
            "rating": show.get("vote_average", 0.0),
            "genres": genres,
            "media_type": "series",
            "source": "tmdb",
        }

    except Exception as e:
        logger.error(f"TMDB TV details error: {e}")
        return None
