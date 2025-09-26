from mcp.server.fastmcp import FastMCP
import logging
from requests import get
import json
from typing import Any, Dict, List, Optional, Union
from fastapi import FastAPI
import httpx
from pydantic import BaseModel

mcp = FastMCP("movies")

BASE_URL = "https://yts.mx/api/v2/list_movies.json"

class Movie(BaseModel):
    title: str
    year: int
    rating: float
    url: str
    summary: str

class MovieDetailResponse(BaseModel):
    title: str
    year: int
    rating: float
    url: str
    summary: str
    genres: List[str]
    language: str
    runtime: int

@mcp.tool()
async def get_movies_info(genre: str, quantity: Optional[int], sorted: Optional[str]) -> Union[List[Movie], Dict[str, str]]:
    """
    Get the best movies of a given genre (sorted by rating).

    Args:
        genre: Movie genre (e.g. "action", "comedy", "drama")
        quantity: Number of movies to retrieve (default: 10)
        sorted: Sorting order (e.g. "rating", "year", "title"). Default is "rating".

    Returns:
        A list of up to quantity movies with keys: title, year, rating, url, summary.
    """

    try:
        async with httpx.AsyncClient(timeout=10) as client:

            paramsObject = {
                "genre": genre,
                "limit": quantity if quantity else 10,
                "sort_by": sorted if sorted else "rating"
            }

            response = await client.get(
                BASE_URL,
                params=paramsObject
            )

        if response.status_code != 200:
            return []

        data = response.json()
        movies = data.get("data", {}).get("movies", [])[:10]

        results = []

        for movie in movies:
            results.append(Movie(
                title=movie.get("title", "Unknown"),
                year=movie.get("year", "N/A"),
                rating=movie.get("rating", 0),
                url=movie.get("url", ""),
                summary=movie.get("summary", "")
            ))

        return results

    except httpx.RequestError as e:
        return {
            "error": f"An error occurred while requesting data: {str(e)}"
        }
    except Exception as e:
        return {
            "error": f"An unexpected error occurred: {str(e)}"
        }


@mcp.tool()
def get_movie_info(title: str) -> Union[MovieDetailResponse, Dict[str, str]]:
    """
    Get detailed information about a specific movie by title.

    Args:
        title: The title of the movie to search for.

    Returns:
        A dictionary with detailed information about the movie, including keys: title, year, rating, url, summary, genres, language, runtime.
    """

    try:
        paramsObject = {
            "query_term": title
        }

        requestURL = f"{BASE_URL}?query_term={title}"

        response = get(requestURL)

        if response.status_code != 200:
            return {"error": "Failed to retrieve data from the movie API."}

        data = response.json()
        movies = data.get("data", {}).get("movies", [])

        if not movies:
            return {"error": f"No movie found with the title '{title}'."}

        movie = movies[0]

        return {
            "title": movie.get("title", "Unknown"),
            "year": movie.get("year", "N/A"),
            "rating": movie.get("rating", 0),
            "url": movie.get("url", ""),
            "summary": movie.get("summary", ""),
            "genres": movie.get("genres", []),
            "language": movie.get("language", "N/A"),
            "runtime": movie.get("runtime",0 )
        }

    except Exception as e:
        return {
            "error": f"An unexpected error occurred: {str(e)}"
        }

if __name__ == "__main__":
    mcp.run(transport="stdio")
