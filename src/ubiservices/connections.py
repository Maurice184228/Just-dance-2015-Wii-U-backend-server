from typing import Any


def build_connection_search_response(
    profile_ids: list[str],
    applications: list[str] | None = None,
    message_types: list[str] | None = None,
    limit: int = 50,
    offset: int = 0,
) -> dict[str, Any]:
    return {
        "limit": limit,
        "offset": offset,
        "connections": [],
    }