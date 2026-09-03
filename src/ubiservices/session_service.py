from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from uuid import uuid4

from src.ubiservices.session_info import SessionInfo
from src.ubiservices.player_credentials import PlayerCredentials


@dataclass
class ServerSession:
    session: SessionInfo
    player_credentials: PlayerCredentials
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

        server_token = str(uuid4())
        server_ticket = str(uuid4())

        session = SessionInfo(
            session_id=str(uuid4()),
            profile_id=str(uuid4()),
            user_id=str(uuid4()),
            product_id="BJDE41",
            space_id="jd2015",
            environment="Prod",
            token=server_token,
            ticket=server_ticket,
            account_issues=[],
            name_on_platform=name_on_platform,
            has_accepted_legal_optins=True,
            expiration=int(expiration.timestamp()),
            server_time=int(now.timestamp()),
            client_ip=client_ip,
            initialize_user=True,
            platform_type="WiiU",
        )

        # Create the separate PlayerCredentials state.
        player_credentials = PlayerCredentials(
            independent_service_id="",
            token_wiiu="",
            principal_id_wiiu="",
            account_id_wiiu="",
            ticket=server_ticket,
            user_id=session.user_id,
            token=server_token,
            name_on_platform=name_on_platform,
            accepted_opt_ins=session.has_accepted_legal_optins,
            expiration=session.expiration,
        )

        state = ServerSession(
            session=session,
            player_credentials=player_credentials,
            source_auth_type=source_auth_type,
        )

        self._sessions[auth_key] = state
        return state

    def find(self, session_id: str) -> ServerSession | None:
        for state in self._sessions.values():
            if state.session.session_id == session_id:
                return state

        return None