from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class SessionInfo:
    session_id: str
    profile_id: str
    user_id: str
    product_id: str
    space_id: str
    environment: str
    token: str
    ticket: str
    account_issues: list[Any]
    name_on_platform: str
    has_accepted_legal_optins: bool
    expiration: int
    server_time: int
    client_ip: str | None
    initialize_user: bool
    platform_type: str
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "sessionId": self.session_id,
            "profileId": self.profile_id,
            "userId": self.user_id,
            "productId": self.product_id,
            "spaceId": self.space_id,
            "environment": self.environment,
            "token": self.token,
            "ticket": self.ticket,
            "accountIssues": self.account_issues,
            "nameOnPlatform": self.name_on_platform,
            "hasAcceptedLegalOptins": self.has_accepted_legal_optins,
            "expiration": self.expiration,
            "serverTime": self.server_time,
            "clientIp": self.client_ip,
            "initializeUser": self.initialize_user,
            "platformType": self.platform_type,
        }