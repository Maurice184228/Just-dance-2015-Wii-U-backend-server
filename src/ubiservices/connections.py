from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any


@dataclass
class ConnectionInfo:
    contact_protocol: str
    created_date: str
    profile_id: str
    application_id: str
    process_id: str
    connection_id: str
    contact_url: str
    last_modified_date: str
    message_types: list[str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "contactProtocol": self.contact_protocol,
            "createdDate": self.created_date,
            "profileId": self.profile_id,
            "applicationId": self.application_id,
            "processId": self.process_id,
            "connectionId": self.connection_id,
            "contactUrl": self.contact_url,
            "lastModifiedDate": self.last_modified_date,
            "messageTypes": self.message_types,
        }


def build_connection_search_response(
    profile_ids: list[str],
    applications: list[str] | None = None,
    message_types: list[str] | None = None,
    limit: int = 50,
    offset: int = 0,
) -> dict[str, Any]:
    if not profile_ids:
        raise ValueError(
            "The profileIds container MUST contain at least 1 profile id."
        )

    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    connections: list[dict[str, Any]] = []

    for profile_id in profile_ids:
        connection = ConnectionInfo(
            contact_protocol="websocket",
            created_date=now,
            profile_id=profile_id,
            application_id="3133a1ba-bf7b-443b-9e8a-f1d5f3b2ac7b",
            process_id="jd2015-wiiu",
            connection_id="",
            contact_url="/websocket/server",
            last_modified_date=now,
            message_types=message_types or [],
        )

        connections.append(connection.to_dict())

    return {
        "limit": limit,
        "offset": offset,
        "connections": connections,
    }