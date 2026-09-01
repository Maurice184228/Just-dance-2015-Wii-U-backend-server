from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class PRUDPFrame:
    raw: bytes

    marker: bytes
    message_type: int
    flags: int
    session_byte: Optional[int]

    def describe(self) -> str:
        return (
            f"PRUDPFrame("
            f"marker={self.marker.hex()}, "
            f"type=0x{self.message_type:02x}, "
            f"flags=0x{self.flags:02x}, "
            f"session_byte={self.session_byte!r}, "
            f"length={len(self.raw)}"
            f")"
        )


def parse_frame(data: bytes) -> PRUDPFrame:
    if len(data) < 4:
        raise ValueError("Packet too short to contain PRUDP framing")

    marker = data[:2]

    # We currently observe:
    #   af a1  -> Wii U side
    #   a1 af  -> remote side
    #
    # Treat this as an observed framing marker for now.
    if marker not in (b"\xaf\xa1", b"\xa1\xaf"):
        raise ValueError(
            f"Unknown packet marker: {marker.hex()}"
        )

    message_type = data[2]
    flags = data[3]

    session_byte = data[4] if len(data) >= 5 else None

    return PRUDPFrame(
        raw=data,
        marker=marker,
        message_type=message_type,
        flags=flags,
        session_byte=session_byte,
    )