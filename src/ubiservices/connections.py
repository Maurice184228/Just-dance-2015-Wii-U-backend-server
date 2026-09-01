from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class ConnectionInfo:
    application_id: str
    profile_id: str
    contact_protocol: str
    created_time: str
    connection_id: str
    contact_url: str
    message_types: list[str]
    json_data: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "applicationId": self.application_id,
            "profileId": self.profile_id,
            "contactProtocol": self.contact_protocol,
            "createdTime": self.created_time,
            "connectionId": self.connection_id,
            "contactUrl": self.contact_url,
            "messageTypes": self.message_types,
            "jsonData": self.json_data,
        }


def build_connection_info(
    *,
    application_id: str,
    profile_id: str,
    contact_protocol: str,
    created_time: str,
    connection_id: str,
    contact_url: str,
    message_types: list[str] | None = None,
    json_data: dict[str, Any] | None = None,
) -> ConnectionInfo:
    return ConnectionInfo(
        application_id=application_id,
        profile_id=profile_id,
        contact_protocol=contact_protocol,
        created_time=created_time,
        connection_id=connection_id,
        contact_url=contact_url,
        message_types=message_types or [],
        json_data=json_data or {},
    )