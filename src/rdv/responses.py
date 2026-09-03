from __future__ import annotations

from .protocol import PRUDPv0Packet


KNOWN_RESPONSES: dict[int, bytes] = {
    0x0061: bytes.fromhex(
        "a1af91007aa439da34010000000000000050"
    ),
}


def build_response(packet: PRUDPv0Packet) -> bytes | None:
    return KNOWN_RESPONSES.get(packet.operation)