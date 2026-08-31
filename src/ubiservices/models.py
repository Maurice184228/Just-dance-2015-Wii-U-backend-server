from dataclasses import dataclass
from typing import Optional


@dataclass
class SessionInfo:
    session_id: str
    profile_id: str
    space_id: str
    environment: str
    platform_type: str
    expiration: Optional[int] = None
    client_ip: Optional[str] = None


@dataclass
class PlayerCredentials:
    token: str
    principal_id: Optional[str] = None
    account_id: Optional[str] = None
    user_id: Optional[str] = None
    name_on_platform: Optional[str] = None