from __future__ import annotations

from .protocol import PRUDPv0Packet


KNOWN_RESPONSES: dict[int, bytes] = {
    0x0040: bytes.fromhex(
        "a1af900000000000000000a00432db000099"
    ),
}


def build_response(packet: PRUDPv0Packet) -> bytes | None:
    if packet.source != 0xAF:
        return None

    if packet.destination != 0xA1:
        return None

    if packet.operation == 0x0040:
        if packet.session_id != 0x00:
            return None

        return KNOWN_RESPONSES[0x0040]

    if packet.operation == 0x0061:
        if packet.session_id != 0x7A:
            return None

        if len(packet.payload) != 4:
            return None

        response = bytearray()

        response.append(0xA1)
        response.append(0xAF)
        response.extend((0x0091).to_bytes(2, "little"))
        response.append(packet.session_id)
        response.extend(packet.payload)
        response.extend(packet.sequence_id.to_bytes(2, "little"))
        response.extend(b"\x00" * 6)
        response.append(0x50)

        return bytes(response)

    return None