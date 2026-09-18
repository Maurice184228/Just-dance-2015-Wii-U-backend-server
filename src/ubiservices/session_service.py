from __future__ import annotations

import base64
import secrets
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from uuid import NAMESPACE_URL, uuid4, uuid5

from src.ubiservices.session_info import SessionInfo
from src.ubiservices.player_credentials import PlayerCredentials


@dataclass
class ServerSession:
    session: SessionInfo
    player_credentials: PlayerCredentials
    source_auth_type: str


def _ubi_datetime(value: datetime) -> str:
    return value.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f0Z")


def _opaque_token(size: int) -> str:
    return base64.b64encode(secrets.token_bytes(size)).decode("ascii")


class SessionService:
    def __init__(self) -> None:
        self._sessions: dict[str, ServerSession] = {}

    def create_or_get(
        self,
        auth_key: str,
        *,
        genome_id: str,
        id_on_platform: str,
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

        server_token = _opaque_token(16)
        server_ticket = _opaque_token(32)

        profile_id = str(
            uuid5(
                NAMESPACE_URL,
                f"ubiservices:profile:{genome_id}:{id_on_platform}",
            )
        )
        user_id = str(
            uuid5(
                NAMESPACE_URL,
                f"ubiservices:user:{genome_id}:{id_on_platform}",
            )
        )
        space_id = str(
            uuid5(
                NAMESPACE_URL,
                f"ubiservices:space:{genome_id}",
            )
        )

        session = SessionInfo(
            session_id=str(uuid4()),
            profile_id=profile_id,
            user_id=user_id,
            space_id=space_id,
            environment="Prod",
            token=server_token,
            ticket=server_ticket,
            account_issues=None,
            name_on_platform=name_on_platform,
            has_accepted_legal_optins=True,
            expiration=_ubi_datetime(expiration),
            server_time=_ubi_datetime(now),
            client_ip=client_ip,
            initialize_user=True,
            platform_type="WiiU",
        )

        wiiu_token = ""

        if auth_key.startswith("wiiu t="):
            wiiu_token = auth_key[len("wiiu t="):].strip()

        player_credentials = PlayerCredentials(
            independent_service_id="",
            token_wiiu=wiiu_token,
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
