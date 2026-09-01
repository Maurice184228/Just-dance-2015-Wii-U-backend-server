from __future__ import annotations

from dataclasses import dataclass


@dataclass
class PRUDPv0Packet:
    raw: bytes

    source: int
    destination: int
    packet_type: int
    flags: int
    session_id: int
    signature: bytes
    sequence_id: int
    payload: bytes
    checksum: int

    def describe(self) -> str:
        return (
            "PRUDPv0Packet("
            f"source=0x{self.source:02x}, "
            f"destination=0x{self.destination:02x}, "
            f"type=0x{self.packet_type:02x}, "
            f"flags=0x{self.flags:02x}, "
            f"session_id=0x{self.session_id:02x}, "
            f"sequence_id={self.sequence_id}, "
            f"payload_length={len(self.payload)}, "
            f"checksum=0x{self.checksum:02x}"
            ")"
        )


def parse_v0(data: bytes) -> PRUDPv0Packet:
    if len(data) < 12:
        raise ValueError("PRUDPv0 packet is too short")

    source = data[0]
    destination = data[1]

    if (source, destination) not in (
        (0xAF, 0xA1),
        (0xA1, 0xAF),
    ):
        raise ValueError(
            f"Unexpected PRUDPv0 direction: "
            f"{source:02x} {destination:02x}"
        )

    type_flags = int.from_bytes(data[2:4], "little")

    packet_type = type_flags & 0x0F
    flags = (type_flags >> 4) & 0x0FFF

    session_id = data[4]

    signature = data[5:9]

    sequence_id = int.from_bytes(
        data[9:11],
        "little",
    )

    checksum = data[-1]

    payload = data[11:-1]

    return PRUDPv0Packet(
        raw=data,
        source=source,
        destination=destination,
        packet_type=packet_type,
        flags=flags,
        session_id=session_id,
        signature=signature,
        sequence_id=sequence_id,
        payload=payload,
        checksum=checksum,
    )