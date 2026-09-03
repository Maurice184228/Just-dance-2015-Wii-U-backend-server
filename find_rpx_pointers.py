from pathlib import Path
import struct

RPX = Path.home() / "Downloads" / "decompressed_output.rpx"
data = RPX.read_bytes()

TARGETS = {
    0x100C4C3F: "JobCreateSession::reportOutcome",
    0x100C4BCB: "JobCreateSession::createSession",
    0x100C49CB: "JobLogin::processConsoleTicket",
    0x100C48E7: "JobLogin::processPostLogin",
    0x100C497F: "JobRequestConsoleTicket::initialize",
    0x100C4E43: "JobRequestConsoleTicket::waitForFetchToken",
}

print("RPX pointer search")
print("=================")

for target, name in TARGETS.items():
    raw = struct.pack(">I", target)

    hits = []

    start = 0

    while True:
        pos = data.find(raw, start)

        if pos == -1:
            break

        hits.append(pos)
        start = pos + 1

    print()
    print(name)
    print(f"target address: 0x{target:08x}")
    print(f"raw pointer hits: {len(hits)}")

    for pos in hits[:50]:
        print(f"  file offset: 0x{pos:08x}")

print()
print("Search complete.")
