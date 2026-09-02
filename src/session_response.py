from __future__ import annotations

from typing import Any

from src.ubiservices.session_state import SessionState


def build_create_session_response(
    state: SessionState,
) -> dict[str, Any]:
    return state.session_info.to_dict()