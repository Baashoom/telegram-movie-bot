#!/bin/bash

# Quick start script for Movie Bot

echo "🎬 Movie Bot - Quick Start"
echo "=========================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9+ first."
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found!"
    echo "📝 Please copy .env.example to .env and fill in your API keys:"
    echo "   cp .env.example .env"
    echo "   nano .env"
    echo ""
    echo "Required API keys:"
    echo "  1. Telegram Bot Token (from @BotFather)"
    echo "  2. TMDB API Key (from themoviedb.org)"
    echo "  3. YouTube API Key (from Google Cloud Console)"
    exit 1
fi

# Start the bot
echo "🚀 Starting Movie Bot..."
python bot.py
