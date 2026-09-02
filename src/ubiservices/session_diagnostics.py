from __future__ import annotations

from typing import Any


def validate_create_session_response(
    response: dict[str, Any],
) -> list[str]:
    required = {
        "sessionId": str,
        "profileId": str,
        "userId": str,
        "productId": str,
        "spaceId": str,
        "environment": str,
        "token": str,
        "ticket": str,
        "accountIssues": list,
        "nameOnPlatform": str,
        "hasAcceptedLegalOptins": bool,
        "expiration": int,
        "serverTime": int,
        "initializeUser": bool,
        "platformType": str,
    }

    errors: list[str] = []

    for field, expected_type in required.items():
        if field not in response:
            errors.append(f"missing field: {field}")
            continue

        if not isinstance(response[field], expected_type):
            errors.append(
                f"{field}: expected {expected_type.__name__}, "
                f"got {type(response[field]).__name__}"
            )

    return errors