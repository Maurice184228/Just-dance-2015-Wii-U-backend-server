from uuid import uuid4

from .models import SessionInfo


class SessionStore:
    def __init__(self) -> None:
        self._sessions: dict[str, SessionInfo] = {}

    def create(
        self,
        profile_id: str,
        space_id: str,
        environment: str,
        platform_type: str,
    ) -> SessionInfo:
        session_id = str(uuid4())

        session = SessionInfo(
            session_id=session_id,
            profile_id=profile_id,
            space_id=space_id,
            environment=environment,
            platform_type=platform_type,
        )

        self._sessions[session_id] = session
        return session

    def get(self, session_id: str) -> SessionInfo | None:
        return self._sessions.get(session_id)