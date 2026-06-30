# Telegram Movie Search Bot

A Telegram bot that searches for movies and series when mentioned or when a user sends a title. Searches IMDb first, then TMDB, and provides detailed information including poster, rating, genres, and trailer link.

## Features

- Search movies and series by title
- Support for year-specific searches (e.g., "Inception 2010")
- Poster image display
- Rating information
- Genre hashtags
- "Watch Trailer" button linking to YouTube
- Works in both group and private chats
- Persian language support (basic)

## Setup Instructions

### 1. Get API Keys

#### Telegram Bot Token
1. Open Telegram and search for @BotFather
2. Send `/newbot` command
3. Choose a name and username for your bot
4. Copy the API token

#### TMDB API Key (Free)
1. Go to https://www.themoviedb.org/
2. Create a free account
3. Go to Settings → API → Create API Key
4. Choose "Developer" and fill in basic info
5. Copy the API Key

#### YouTube API Key (Free Tier)
1. Go to https://console.cloud.google.com/
2. Create a new project
3. Enable "YouTube Data API v3"
4. Create credentials → API Key
5. Copy the API key

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Copy `.env.example` to `.env` and fill in your API keys:

```bash
cp .env.example .env
```

Edit `.env` file:
```
BOT_TOKEN=your_bot_token_here
TMDB_API_KEY=your_tmdb_api_key_here
YOUTUBE_API_KEY=your_youtube_api_key_here
```

### 4. Run the Bot

```bash
python bot.py
```

## Usage

### In Private Chat
Simply send a movie or series name to the bot.

### In Groups
Mention the bot with @username followed by the movie name:
```
@your_bot_name Inception
```

## Examples

- `Inception` - Search for the movie "Inception"
- `Inception 2010` - Search for the 2010 version
- `Breaking Bad` - Search for the TV series
- `The Dark Knight 2008` - Search with year

## Output Format

The bot will respond with:
- Title and year
- Poster image
- Plot summary (1-2 sentences)
- Rating
- #film or #series hashtag
- Genre hashtags
- "Watch Trailer" button

## Deployment

### Local/VPS (Recommended)
Run on your own machine or VPS:
```bash
python bot.py
```

### Docker
Create a Dockerfile:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "bot.py"]
```

Build and run:
```bash
docker build -t movie-bot .
docker run -d --name movie-bot movie-bot
```

## Rate Limiting

The bot implements basic rate limiting (5 searches per user per minute) to prevent abuse.

## Error Handling

- Graceful fallback between IMDb and TMDB services
- Clear "not found" message when both services fail
- Retry logic for network errors
- Proper error messages for users

## License

This project is open source and available for personal use.
