from dataclasses import dataclass
from typing import Optional, List


@dataclass
class MovieResult:
    title: str
    year: Optional[str]
    poster_url: str
    plot: str
    rating: float
    rating_source: str  # "imdb" or "tmdb"
    genres: List[str]
    trailer_url: Optional[str]
    media_type: str  # "film" or "series"
    original_title: Optional[str] = None
