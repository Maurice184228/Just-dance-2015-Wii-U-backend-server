from __future__ import annotations

from .protocol import PRUDPv0Packet


KNOWN_RESPONSES: dict[int, bytes] = {
    0x0061: bytes.fromhex(
        "a1af91007aa439da34010000000000000050"
    ),
}


def build_response(packet: PRUDPv0Packet) -> bytes | None:
    if packet.source != 0xAF:
        return None

    if packet.destination != 0xA1:
        return None

    if packet.session_id != 0x7A:
        return None

    return KNOWN_RESPONSES.get(packet.operation)