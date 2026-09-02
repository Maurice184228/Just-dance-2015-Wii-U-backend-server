from __future__ import annotations

from dataclasses import dataclass

from src.ubiservices.player_credentials import PlayerCredentials
from src.ubiservices.session_info import SessionInfo


@dataclass
class SessionState:
    session_info: SessionInfo
    player_credentials: PlayerCredentials