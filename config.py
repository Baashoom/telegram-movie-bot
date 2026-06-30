import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
BOT_TOKEN = os.getenv("BOT_TOKEN")
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

# Rate limiting
MAX_SEARCHES_PER_USER_PER_MINUTE = 5

# Search settings
TMDB_BASE_URL = "https://api.themoviedb.org/3"
YOUTUBE_BASE_URL = "https://www.googleapis.com/youtube/v3"
IMDB_SEARCH_URL = "https://www.imdb.com/find"
IMDB_BASE_URL = "https://www.imdb.com"

# Poster sizes
TMDB_POSTER_SIZE = "w500"

# Cache settings (in seconds)
CACHE_EXPIRY = 86400  # 24 hours
