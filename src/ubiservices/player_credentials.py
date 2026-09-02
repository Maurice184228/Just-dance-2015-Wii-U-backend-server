from __future__ import annotations

from dataclasses import dataclass


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