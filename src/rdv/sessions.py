from __future__ import annotations

from dataclasses import dataclass

from .protocol import PRUDPv0Packet


@dataclass
class RDVSession:
    session_id: int
    packet_signature: bytes
    last_sequence_id: int
    last_operation: int
    packets_received: int = 0

    def update(self, packet: PRUDPv0Packet) -> None:
        self.packet_signature = packet.packet_signature
        self.last_sequence_id = packet.sequence_id
        self.last_operation = packet.operation
        self.packets_received += 1


class RDVSessionStore:
    def __init__(self) -> None:
        self._sessions: dict[int, RDVSession] = {}

    def get(self, session_id: int) -> RDVSession | None:
        return self._sessions.get(session_id)

    def get_or_create(self, packet: PRUDPv0Packet) -> RDVSession:
        session = self._sessions.get(packet.session_id)

        if session is None:
            session = RDVSession(
                session_id=packet.session_id,
                packet_signature=packet.packet_signature,
                last_sequence_id=packet.sequence_id,
                last_operation=packet.operation,
            )
            self._sessions[packet.session_id] = session

        session.update(packet)
        return session

    def remove(self, session_id: int) -> None:
        self._sessions.pop(session_id, None)

    def clear(self) -> None:
        self._sessions.clear()

    def all(self) -> list[RDVSession]:
        return list(self._sessions.values())