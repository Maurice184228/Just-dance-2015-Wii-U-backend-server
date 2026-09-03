from __future__ import annotations

from dataclasses import dataclass

from .protocol import PRUDPv0Packet


@dataclass
class RDVSession:
    session_id: int
    packet_signature: bytes
    last_sequence_id: int
    last_operation: int
    client_host: str
    client_port: int
    packets_received: int = 0

    def update(
        self,
        packet: PRUDPv0Packet,
        addr: tuple[str, int],
    ) -> None:
        self.packet_signature = packet.packet_signature
        self.last_sequence_id = packet.sequence_id
        self.last_operation = packet.operation
        self.client_host = addr[0]
        self.client_port = addr[1]
        self.packets_received += 1


class RDVSessionStore:
    def __init__(self) -> None:
        self._sessions: dict[tuple[str, int, int], RDVSession] = {}

    def get(
        self,
        session_id: int,
        addr: tuple[str, int],
    ) -> RDVSession | None:
        return self._sessions.get((addr[0], addr[1], session_id))

    def get_or_create(
        self,
        packet: PRUDPv0Packet,
        addr: tuple[str, int],
    ) -> RDVSession:
        key = (addr[0], addr[1], packet.session_id)
        session = self._sessions.get(key)

        if session is None:
            session = RDVSession(
                session_id=packet.session_id,
                packet_signature=packet.packet_signature,
                last_sequence_id=packet.sequence_id,
                last_operation=packet.operation,
                client_host=addr[0],
                client_port=addr[1],
            )
            self._sessions[key] = session

        session.update(packet, addr)
        return session

    def remove(
        self,
        session_id: int,
        addr: tuple[str, int],
    ) -> None:
        self._sessions.pop(
            (addr[0], addr[1], session_id),
            None,
        )

    def clear(self) -> None:
        self._sessions.clear()

    def all(self) -> list[RDVSession]:
        return list(self._sessions.values())