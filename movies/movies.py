from mcp.server.fastmcp import FastMCP
import logging
from requests import get
import json
from typing import Any, Dict, List
from fastapi import FastAPI
import httpx

mcp = FastMCP("movies")

app = FastAPI()

BASE_URL = "https://yts.mx/api/v2/list_movies.json"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s"
)
logger = logging.getLogger("movies_tool")

@app.get("/movies/{genre}")
@mcp.tool()
async def get_movies_info(genre: str, quantity: int, sorted: str) -> List[Dict[str, Any]]:
    """
    Get the best movies of a given genre (sorted by rating).

    Args:
        genre: Movie genre (e.g. "action", "comedy", "drama")
        quantity: Number of movies to retrieve (default: 10)
        sorted: Sorting order (e.g. "rating", "year", "title"). Default is "rating".

    Returns:
        A list of up to quantity movies with keys: title, year, rating, url, summary.
    """
    logger.info(f"Fetching movies for genre: {genre}")

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(
                BASE_URL,
                params={"genre": genre, "limit": quantity, "sort_by": "year"}
            )

        if response.status_code != 200:
            logger.warning(f"Failed request with status {response.status_code}")
            return []

        data = response.json()
        movies = data.get("data", {}).get("movies", [])[:10]

        results = []

        for movie in movies:
            results.append({
                "title": movie.get("title", "Unknown"),
                "year": movie.get("year", "N/A"),
                "rating": movie.get("rating", 0),
                "url": movie.get("url", ""),
                "summary": movie.get("summary", "")
        })

        return results

    except httpx.RequestError as e:
        logger.exception(f"Network error while fetching movies: {e}")
        return []
    except Exception as e:
        logger.exception(f"Unexpected error while fetching movies: {e}")
        return []

if __name__ == "__main__":
    logger.info("Starting MCP server...")
    mcp.run(transport="stdio")
    app.run()
