from __future__ import annotations

import asyncio
from dataclasses import dataclass

from .protocol import PRUDPv0Packet, parse_v0
from .responses import build_response
from .sessions import RDVSessionStore

from .operations import get_operation
APPLICATION_ID = "3133a1ba-bf7b-443b-9e8a-f1d5f3b2ac7b"
BUILD_ID = "JD2015WIIU_E163180"
SANDBOX_NAME = "JustDance6 DEV"
SANDBOX_KEY = "wmG82823Ek9f"

# Keep False while discovering the real RDV packet exchange.
RESPOND_TO_PACKETS = False


@dataclass
class RDVServer:
    host: str = "0.0.0.0"
    port: int = 14000

    def __post_init__(self) -> None:
        self.sessions = RDVSessionStore()


class PRUDPProtocol(asyncio.DatagramProtocol):
    def __init__(self, server: RDVServer) -> None:
        self.server = server
        self.transport: asyncio.DatagramTransport | None = None

    def connection_made(
        self,
        transport: asyncio.BaseTransport,
    ) -> None:
        self.transport = transport  # type: ignore[assignment]

        print()
        print("============================================================")
        print(" JD2015 Wii U / RendezVous")
        print("============================================================")
        print(
            f"  UDP listening : "
            f"{self.server.host}:{self.server.port}"
        )
        print(f"  Application   : {APPLICATION_ID}")
        print(f"  Build ID      : {BUILD_ID}")
        print(f"  Sandbox       : {SANDBOX_NAME}")
        print(f"  Sandbox key   : {SANDBOX_KEY}")
        print(f"  Responding    : {RESPOND_TO_PACKETS}")
        print("============================================================")
        print()

    def datagram_received(
        self,
        data: bytes,
        addr: tuple[str, int],
    ) -> None:
        print()
        print("[RDV] Packet received")
        print(f"  from   : {addr[0]}:{addr[1]}")
        print(f"  bytes  : {len(data)}")
        print(f"  raw    : {data.hex()}")

        print("  hex dump:")
        for offset in range(0, len(data), 16):
            chunk = data[offset:offset + 16]

            hex_part = " ".join(f"{b:02x}" for b in chunk)
            ascii_part = "".join(
                chr(b) if 32 <= b <= 126 else "."
                for b in chunk
            )

            print(
                f"    {offset:04x}  "
                f"{hex_part:<47}  "
                f"|{ascii_part}|"
            )

        print()

        try:
            packet = parse_v0(data)
        except ValueError as exc:
            print(f"  parse error: {exc}")
            return

        existing_session = self.server.sessions.get(
            packet.session_id,
            addr,
        )

        if existing_session is not None:
            if not existing_session.accepts_sequence(
                packet.sequence_id
            ):
                print("[RDV] Sequence rejected")
                print(
                    f"  expected: "
                    f"{existing_session.next_sequence_id}"
                )
                print(
                    f"  received: "
                    f"{packet.sequence_id}"
                )
                return

        session = self.server.sessions.get_or_create(
            packet,
            addr,
        )
        
        operation = get_operation(packet.operation)

        print("[RDV] Operation")

        if operation is not None:
            print(f"  name: {operation.name}")
            print(f"  description: {operation.description}")
        else:
            print(f"  unknown: 0x{packet.operation:04x}")

        print(f"  source : 0x{packet.source:02x}")
        print(f"  dest   : 0x{packet.destination:02x}")
        print(f"  op     : 0x{packet.operation:04x}")
        print(f"  session: 0x{packet.session_id:02x}")
        print(f"  seq    : {packet.sequence_id}")
        print(f"  payload: {packet.payload.hex()}")

        print("[RDV] Session state")
        print(f"  packets: {session.packets_received}")
        print(
            f"  last operation: "
            f"0x{session.last_operation:04x}"
        )
        
        if RESPOND_TO_PACKETS:
            # Known request/response pair from the captured fixture.
            response = build_response(packet)

        if response is not None:
                print(
                    f"[RDV] Sending response for "
                    f"0x{packet.operation:04x}"
                )
                print(f"  bytes: {len(response)}")

                if self.transport is not None:
                    self.transport.sendto(response, addr)
        else:
            print("[RDV] Response disabled; packet captured only.")
                
    def error_received(self, exc: Exception) -> None:
        print(f"[RDV] UDP error: {exc}")

    def connection_lost(self, exc: Exception | None) -> None:
        print("[RDV] UDP socket closed")


async def run_server(
    host: str = "0.0.0.0",
    port: int = 14000,
) -> None:
    server = RDVServer(host=host, port=port)

    loop = asyncio.get_running_loop()

    transport, _ = await loop.create_datagram_endpoint(
        lambda: PRUDPProtocol(server),
        local_addr=(host, port),
    )

    try:
        await asyncio.Future()
    finally:
        transport.close()


def main() -> None:
    asyncio.run(run_server())


if __name__ == "__main__":
    main()