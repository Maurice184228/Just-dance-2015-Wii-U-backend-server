from __future__ import annotations

from dataclasses import dataclass


@dataclass
class PRUDPv0Packet:
    raw: bytes

    source: int
    destination: int
    operation: int
    session_id: int
    packet_signature: bytes
    sequence_id: int
    payload: bytes
    checksum: int

    def describe(self) -> str:
        return (
            "PRUDPv0Packet("
            f"source=0x{self.source:02x}, "
            f"destination=0x{self.destination:02x}, "
            f"operation=0x{self.operation:04x}, "
            f"session_id=0x{self.session_id:02x}, "
            f"packet_signature={self.packet_signature.hex()}, "
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
            f"Unexpected PRUDP direction: "
            f"{source:02x} {destination:02x}"
        )

    operation = int.from_bytes(
        data[2:4],
        byteorder="little",
    )

    session_id = data[4]

    packet_signature = data[5:9]

    sequence_id = int.from_bytes(
        data[9:11],
        byteorder="little",
    )

    checksum = data[-1]

    payload = data[11:-1]

    return PRUDPv0Packet(
        raw=data,
        source=source,
        destination=destination,
        operation=operation,
        session_id=session_id,
        packet_signature=packet_signature,
        sequence_id=sequence_id,
        payload=payload,
        checksum=checksum,
    )