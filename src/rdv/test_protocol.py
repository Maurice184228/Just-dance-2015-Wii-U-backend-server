from __future__ import annotations

from .protocol import parse_v0


PACKETS = {
    593: bytes.fromhex(
        "afa14000000000000000000000000097"
    ),

    594: bytes.fromhex(
        "a1af900000000000000000a00432db000099"
    ),

    595: bytes.fromhex(
        "afa161007aa00432db0100a439da34d2"
    ),

    597: bytes.fromhex(
        "a1af91007aa439da34010000000000000050"
    ),

    600: bytes.fromhex(
        "afa162007a7a4653f4020000198744db99f82c5005a361fd2a1df280cb62d0c2a7649b2e63efb7"
    ),
}


def main() -> None:
    for packet_number, data in PACKETS.items():
        print(f"\nPacket {packet_number}")
        print(f"Length: {len(data)} bytes")

        try:
            packet = parse_v0(data)

            print(packet.describe())
            print(f"Payload: {packet.payload.hex()}")

        except ValueError as exc:
            print(f"Parse error: {exc}")


if __name__ == "__main__":
    main()
    
    from .sessions import RDVSessionStore


def test_session_store() -> None:
    store = RDVSessionStore()

    print("\nRDV SESSION STORE TEST")
    print("======================")

    for packet_number, data in PACKETS.items():
        packet = parse_v0(data)

        session = store.get_or_create(packet)

        print(
            f"Packet {packet_number}: "
            f"session=0x{session.session_id:02x}, "
            f"operation=0x{session.last_operation:04x}, "
            f"sequence={session.last_sequence_id}, "
            f"packets={session.packets_received}"
        )

    print("\nStored sessions:")

    for session in store.all():
        print(
            f"  session=0x{session.session_id:02x} "
            f"signature={session.packet_signature.hex()} "
            f"last_operation=0x{session.last_operation:04x} "
            f"last_sequence={session.last_sequence_id} "
            f"packets={session.packets_received}"
        )


if __name__ == "__main__":
    main()
    test_session_store()