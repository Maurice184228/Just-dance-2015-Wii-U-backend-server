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

    # The captured 0x0061 request has a 4-byte payload.
    # The captured 0x0091 response uses that payload as
    # its packet signature.
    if len(packet.payload) != 4:
        return None

    response = bytearray()

    response.append(0xA1)
    response.append(0xAF)
    response.extend((0x0091).to_bytes(2, "little"))
    response.append(packet.session_id)

    # Request payload becomes response packet signature.
    response.extend(packet.payload)

    # Echo the request sequence number.
    response.extend(packet.sequence_id.to_bytes(2, "little"))

    # Captured response payload.
    response.extend(b"\x00" * 6)

    # Checksum is not decoded yet.
    response.append(0x50)

    return bytes(response)