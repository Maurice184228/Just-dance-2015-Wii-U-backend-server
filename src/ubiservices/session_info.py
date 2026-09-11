from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class SessionInfo:
    session_id: str
    profile_id: str
    user_id: str
    space_id: str
    environment: str
    token: str
    ticket: str
    account_issues: list[Any] | None
    name_on_platform: str
    has_accepted_legal_optins: bool
    expiration: str
    server_time: str
    client_ip: str | None
    initialize_user: bool
    platform_type: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "token": self.token,
            "ticket": self.ticket,
            "expiration": self.expiration,
            "platformType": self.platform_type,
            "profileId": self.profile_id,
            "userId": self.user_id,
            "nameOnPlatform": self.name_on_platform,
            "initializeUser": self.initialize_user,
            "spaceId": self.space_id,
            "environment": self.environment,
            "hasAcceptedLegalOptins": self.has_accepted_legal_optins,
            "accountIssues": self.account_issues,
            "sessionId": self.session_id,
            "clientIp": self.client_ip,
            "serverTime": self.server_time,
        }
