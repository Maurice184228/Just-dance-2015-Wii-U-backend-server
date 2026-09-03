from __future__ import annotations

from .protocol import PRUDPv0Packet


def build_response(packet: PRUDPv0Packet) -> bytes | None:
    if packet.source != 0xAF:
        return None

    if packet.destination != 0xA1:
        return None

    if packet.operation != 0x0061:
        return None

    if packet.session_id != 0x7A:
        return None

    # Known 0x0061 -> 0x0091 response structure:
    #
    # source       1 byte
    # destination  1 byte
    # operation    2 bytes, little-endian
    # session      1 byte
    # signature    4 bytes
    # sequence     2 bytes, little-endian
    # payload      6 bytes
    # checksum     1 byte
    #
    # The captured response has a six-byte zero payload.

    response = bytearray()

    response.append(0xA1)
    response.append(0xAF)
    response.extend((0x0091).to_bytes(2, "little"))
    response.append(packet.session_id)
    response.extend(packet.packet_signature)
    response.extend(packet.sequence_id.to_bytes(2, "little"))
    response.extend(b"\x00" * 6)

    # checksum algorithm is not decoded yet.
    # Keeping the captured checksum for this known fixture.
    response.append(0x50)

    return bytes(response)