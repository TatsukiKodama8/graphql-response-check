import requests
from typing import List, Tuple

INTROSPECTION_QUERY: str = """
{
  __schema {
    queryType {
      fields {
        name
      }
    }
  }
}
"""

def get_query_names(endpoint: str) -> List[str]:
    """
    Retrieve a list of query operation names using GraphQL introspection.

    Args:
        endpoint (str): GraphQL API endpoint URL.

    Returns:
        List[str]: List of available query operation names.
    """
    try:
        response: requests.Response = requests.post(
            endpoint,
            json={"query": INTROSPECTION_QUERY},
            headers={"Content-Type": "application/json"},
            timeout=5
        )
        if response.status_code != 200:
            raise Exception("Introspection request failed.")
        data: dict = response.json()
        return [field["name"] for field in data["data"]["__schema"]["queryType"]["fields"]]
    except Exception as e:
        print(f"[ERROR] [{endpoint}] Failed to fetch introspection data: {e}")
        return []

def send_graphql_query(endpoint: str, query_name: str) -> bool:
    """
    Send a POST request to the GraphQL endpoint with a basic query.

    Args:
        endpoint (str): GraphQL API endpoint URL.
        query_name (str): Query operation name to be called.

    Returns:
        bool: True if HTTP 200 is returned, False otherwise.
    """
    query: str = f"query {{ {query_name} }}"

    try:
        response: requests.Response = requests.post(
            endpoint,
            json={"query": query},
            headers={"Content-Type": "application/json"},
            timeout=5
        )
        return response.status_code == 200
    except requests.RequestException as e:
        print(f"[ERROR] [{endpoint}] Request failed: {e}")
        return False

def count_query_status(endpoint: str, query_names: List[str]) -> Tuple[int, int]:
    """
    Execute all given query operations and count how many return HTTP 200.

    Args:
        endpoint (str): GraphQL API endpoint URL.
        query_names (List[str]): List of query operation names to check.

    Returns:
        Tuple[int, int]: (ok_count, ng_count)
    """
    ok_count: int = 0
    ng_count: int = 0

    for name in query_names:
        is_ok: bool = send_graphql_query(endpoint, name)
        print(f"{name}: {'OK' if is_ok else 'NG'}")
        if is_ok:
            ok_count += 1
        else:
            ng_count += 1

    return ok_count, ng_count