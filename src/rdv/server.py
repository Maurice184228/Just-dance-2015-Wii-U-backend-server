from __future__ import annotations

import asyncio
from dataclasses import dataclass

from .protocol import PRUDPv0Packet, parse_v0
from .responses import build_response
from .sessions import RDVSessionStore

from .operations import get_operation


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

        print(
            f"[RDV] UDP listening on "
            f"{self.server.host}:{self.server.port}"
        )

    def datagram_received(
        self,
        data: bytes,
        addr: tuple[str, int],
    ) -> None:
        print()
        print("[RDV] Packet received")
        print(f"  from   : {addr[0]}:{addr[1]}")
        print(f"  bytes  : {len(data)}")

        try:
            packet = parse_v0(data)
        except ValueError as exc:
            print(f"  parse error: {exc}")
            return

        session = self.server.sessions.get_or_create(packet)
        
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