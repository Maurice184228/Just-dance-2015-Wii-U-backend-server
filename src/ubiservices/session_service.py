from __future__ import annotations

from datetime import datetime, timezone, timedelta
from typing import Any
from uuid import uuid4

from src.ubiservices.session_info import SessionInfo


class SessionService:
    def __init__(self) -> None:
        self._sessions: dict[str, SessionInfo] = {}

    def create_or_get(
        self,
        auth_key: str,
        *,
        name_on_platform: str,
        client_ip: str | None,
    ) -> SessionInfo:
        existing = self._sessions.get(auth_key)

        if existing is not None:
            return existing

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

        self._sessions[auth_key] = session
        return session

    def find(self, session_id: str) -> SessionInfo | None:
        for session in self._sessions.values():
            if session.session_id == session_id:
                return session

        return None