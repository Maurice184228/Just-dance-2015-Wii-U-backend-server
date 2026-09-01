from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class WebSocketConnectionInfo:
    path: str
    headers: dict[str, str]

    def describe(self) -> str:
        return (
            "WebSocketConnectionInfo("
            f"path={self.path!r}, "
            f"header_count={len(self.headers)}"
            ")"
        )


EXPECTED_HANDSHAKE_HEADERS = (
    "host",
    "upgrade",
    "sec-websocket-key",
    "sec-websocket-version",
    "user-agent",
    "connection",
    "sec-websocket-protocol",
    "sec-websocket-extensions",
)


def capture_handshake(
    path: str,
    headers: dict[str, str],
) -> WebSocketConnectionInfo:
    return WebSocketConnectionInfo(
        path=path,
        headers=dict(headers),
    )


def build_diagnostic_response() -> dict[str, Any]:
    return {
        "status": "accepted",
        "service": "UbiServices-WebSocket",
    }