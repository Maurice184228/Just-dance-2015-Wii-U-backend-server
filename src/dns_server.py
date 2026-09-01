from __future__ import annotations

import socket
from typing import Optional

from dnslib import DNSRecord, RR, A, QTYPE


LISTEN_HOST = "10.0.0.164"
LISTEN_PORT = 53

OVERRIDE_HOST = "api-ubiservices.ubi.com."
OVERRIDE_IP = "10.0.0.164"

UPSTREAM_DNS = [
    ("24.201.245.77", 53),
    ("24.200.243.189", 53),
]


def query_upstream(request: bytes, server: tuple[str, int]) -> Optional[bytes]:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(3)

    try:
        sock.sendto(request, server)
        response, _ = sock.recvfrom(4096)
        return response
    except OSError as exc:
        print(f"[DNS] Upstream error from {server}: {exc}")
        return None
    finally:
        sock.close()


def main() -> None:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((LISTEN_HOST, LISTEN_PORT))

    print(f"[DNS] Listening on {LISTEN_HOST}:{LISTEN_PORT}")
    print(f"[DNS] Override: {OVERRIDE_HOST} -> {OVERRIDE_IP}")

    while True:
        data, client = sock.recvfrom(4096)

        try:
            request = DNSRecord.parse(data)

            if not request.questions:
                continue

            question = request.questions[0]
            qname = str(question.qname).lower()
            qtype = QTYPE[question.qtype]

            print(f"[DNS] {client[0]}:{client[1]} -> {qname} ({qtype})")

            # Only override IPv4 A queries for the Ubisoft hostname.
            if qname == OVERRIDE_HOST and qtype == "A":
                reply = request.reply()
                reply.add_answer(
                    RR(
                        OVERRIDE_HOST,
                        QTYPE.A,
                        rdata=A(OVERRIDE_IP),
                        ttl=30,
                    )
                )

                sock.sendto(reply.pack(), client)

                print(
                    f"[DNS] OVERRIDE {OVERRIDE_HOST} -> {OVERRIDE_IP}"
                )

                continue

            # Forward everything else.
            response = None

            for server in UPSTREAM_DNS:
                response = query_upstream(data, server)
                if response is not None:
                    break

            if response is None:
                print("[DNS] All upstream DNS servers failed.")
                continue

            sock.sendto(response, client)

        except Exception as exc:
            print(f"[DNS] Request handling error: {exc}")


if __name__ == "__main__":
    main()