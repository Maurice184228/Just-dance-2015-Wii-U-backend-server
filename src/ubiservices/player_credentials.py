from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class PlayerCredentials:
    independent_service_id: str
    token_wiiu: str
    principal_id_wiiu: str
    account_id_wiiu: str
    ticket: str
    user_id: str
    token: str
    name_on_platform: str
    accepted_opt_ins: bool
    expiration: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "IndependentServiceId": self.independent_service_id,
            "TokenWiiU": self.token_wiiu,
            "PrincipalIdWiiU": self.principal_id_wiiu,
            "AccountIdWiiU": self.account_id_wiiu,
            "ticket": self.ticket,
            "userId": self.user_id,
            "token": self.token,
            "nameOnPlatform": self.name_on_platform,
            "acceptedOptIns": self.accepted_opt_ins,
            "expiration": self.expiration,
        }