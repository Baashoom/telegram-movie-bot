#!/usr/bin/env python3
"""
Test script for movie bot services.
Run this to verify the services work correctly.
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.search import search_movie, parse_search_query
from services.youtube import search_trailer
from utils.formatters import format_movie_message


def test_parse_query():
    """Test query parsing."""
    print("Testing query parsing...")

    test_cases = [
        ("Inception", ("Inception", None)),
        ("Inception 2010", ("Inception", "2010")),
        ("The Dark Knight (2008)", ("The Dark Knight", "2008")),
        ("@bot Inception", ("Inception", None)),
        ("@bot Inception 2010", ("Inception", "2010")),
    ]

    for query, expected in test_cases:
        result = parse_search_query(query)
        status = "✓" if result == expected else "✗"
        print(f"  {status} '{query}' -> {result}")
        if result != expected:
            print(f"    Expected: {expected}")


def test_search():
    """Test movie search."""
    print("\nTesting movie search...")

    # Test with a well-known movie
    title = "Inception"
    year = "2010"

    print(f"  Searching for: {title} ({year})")
    result = search_movie(title, year)

    if result:
        print(f"  ✓ Found: {result.title} ({result.year})")
        print(f"    Rating: {result.rating}/10")
        print(f"    Genres: {', '.join(result.genres)}")
        print(f"    Poster: {'✓' if result.poster_url else '✗'}")
        print(f"    Trailer: {'✓' if result.trailer_url else '✗'}")

        # Test formatting
        print("\n  Formatted message:")
        print("  " + "-" * 40)
        message = format_movie_message(result)
        for line in message.split("\n"):
            print(f"  {line}")
        print("  " + "-" * 40)
    else:
        print("  ✗ Not found")


def test_trailer():
    """Test trailer search."""
    print("\nTesting trailer search...")

    title = "Inception"
    year = "2010"

    print(f"  Searching trailer for: {title}")
    trailer_url = search_trailer(title, year)

    if trailer_url:
        print(f"  ✓ Found trailer: {trailer_url}")
    else:
        print("  ✗ Trailer not found")


if __name__ == "__main__":
    print("Movie Bot Service Tests")
    print("=" * 50)

    try:
        test_parse_query()
        test_search()
        test_trailer()

        print("\n" + "=" * 50)
        print("All tests completed!")

    except Exception as e:
        print(f"\nError during testing: {e}")
        import traceback
        traceback.print_exc()
