import os
from typing import List

def get_endpoints_from_env() -> List[str]:
    """
    Load GraphQL endpoint list from environment variable GRAPHQL_ENDPOINTS.

    Returns:
        List[str]: List of cleaned endpoint URLs.
    """
    raw = os.getenv("GRAPHQL_ENDPOINTS", "")
    raw = raw.strip('"').strip("'")  # remove surrounding quotes if present
    return [url.strip() for url in raw.split(",") if url.strip()]
