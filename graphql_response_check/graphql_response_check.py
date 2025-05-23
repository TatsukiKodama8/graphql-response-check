#!/usr/bin/env python3
"""
GraphQL Health Check via Introspection

This script connects to one or more GraphQL endpoints, fetches all query operation names
via introspection, and then sends simple query requests to verify HTTP 200 response.
"""
from dotenv import load_dotenv

from graphql_response_check.lib.get_env import get_endpoints_from_env
from graphql_response_check.lib.query import get_query_names, count_query_status

# Load environment variables from .env file
load_dotenv()

# ================== MAIN FUNCTION ==================
def graphql_response_check() -> None:
    """
    Perform GraphQL health check for all endpoints defined in environment.
    """
    endpoints: list[str] = get_endpoints_from_env()

    for endpoint in endpoints:
        print(f"\n========== Checking Endpoint: {endpoint} ==========")
        query_names: list[str] = get_query_names(endpoint)
        print(f"[INFO] Found {len(query_names)} queries: {query_names}")

        ok_count, ng_count = count_query_status(endpoint, query_names)

        print(f"---------- Summary for {endpoint} ----------")
        print(f"Total: {len(query_names)} | OK: {ok_count} | NG: {ng_count}")

