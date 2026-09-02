from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from uuid import uuid4

from src.ubiservices.session_info import SessionInfo


@dataclass
class ServerSession:
    session: SessionInfo
    source_auth_type: str


class SessionService:
    def __init__(self) -> None:
        self._sessions: dict[str, ServerSession] = {}

    def create_or_get(
        self,
        auth_key: str,
        *,
        name_on_platform: str,
        client_ip: str | None,
    ) -> ServerSession:
        existing = self._sessions.get(auth_key)

        if existing is not None:
            return existing

        source_auth_type = (
            "wiiu"
            if auth_key.startswith("wiiu t=")
            else "other"
        )

        now = datetime.now(timezone.utc)
        expiration = now + timedelta(days=1)

        session = SessionInfo(
            session_id=str(uuid4()),
            profile_id=str(uuid4()),
            user_id=str(uuid4()),
            product_id="BJDE41",
            space_id="jd2015",
            environment="Prod",
            token="",
            ticket="",
            account_issues=[],
            name_on_platform=name_on_platform,
            has_accepted_legal_optins=True,
            expiration=int(expiration.timestamp()),
            server_time=int(now.timestamp()),
            client_ip=client_ip,
            initialize_user=True,
            platform_type="WiiU",
        )

        state = ServerSession(
            session=session,
            source_auth_type=source_auth_type,
        )

        self._sessions[auth_key] = state
        return state

    def find(self, session_id: str) -> ServerSession | None:
        for state in self._sessions.values():
            if state.session.session_id == session_id:
                return state

        return None