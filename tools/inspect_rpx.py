from pathlib import Path
import struct

RPX = Path.home() / "Downloads" / "decompressed_output.rpx"
data = RPX.read_bytes()

if data[:4] != b"\x7fELF":
    raise SystemExit("Not an ELF file")

print("ELF magic: OK")
print("Class:", data[4])
print("Data encoding:", data[5])

if data[4] != 1 or data[5] != 2:
    raise SystemExit("Expected ELF32 big-endian")

# ELF32 header
e_shoff = struct.unpack_from(">I", data, 32)[0]
e_shentsize = struct.unpack_from(">H", data, 46)[0]
e_shnum = struct.unpack_from(">H", data, 48)[0]
e_shstrndx = struct.unpack_from(">H", data, 50)[0]

print(f"Section header offset: 0x{e_shoff:x}")
print(f"Section header size:   {e_shentsize}")
print(f"Section count:         {e_shnum}")
print(f"String table index:    {e_shstrndx}")
print()

sections = []

for i in range(e_shnum):
    off = e_shoff + i * e_shentsize

    fields = struct.unpack_from(">IIIIIIIIII", data, off)

    sections.append({
        "index": i,
        "name": fields[0],
        "type": fields[1],
        "flags": fields[2],
        "addr": fields[3],
        "offset": fields[4],
        "size": fields[5],
        "link": fields[6],
        "info": fields[7],
        "align": fields[8],
        "entsize": fields[9],
    })

if not (0 <= e_shstrndx < len(sections)):
    raise SystemExit("Invalid section string-table index")

shstr = sections[e_shstrndx]

shstr_start = shstr["offset"]
shstr_end = shstr_start + shstr["size"]
shstr_data = data[shstr_start:shstr_end]


def section_name(offset: int) -> str:
    if offset >= len(shstr_data):
        return "<bad-name-offset>"

    end = shstr_data.find(b"\x00", offset)

    if end == -1:
        end = len(shstr_data)

    return shstr_data[offset:end].decode(
        "ascii",
        errors="replace",
    )


print("SECTIONS")
print("========")

for s in sections:
    name = section_name(s["name"])

    print(
        f'#{s["index"]:2d} '
        f'{name:24s} '
        f'type=0x{s["type"]:08x} '
        f'flags=0x{s["flags"]:08x} '
        f'file=0x{s["offset"]:08x} '
        f'size=0x{s["size"]:08x} '
        f'addr=0x{s["addr"]:08x}'
    )

print()
print("CANDIDATE CODE SECTIONS")
print("=======================")

for s in sections:
    # SHF_EXECINSTR = 0x4
    if s["flags"] & 0x4:
        name = section_name(s["name"])

        print(
            f'#{s["index"]}: {name} '
            f'file=0x{s["offset"]:08x} '
            f'size=0x{s["size"]:08x} '
            f'addr=0x{s["addr"]:08x}'
        )

print()
print("TARGET STRING LOCATIONS")
print("========================")

targets = [
    (0x0c54ff, "JobCreateSession::reportOutcome"),
    (0x0c548b, "JobCreateSession::createSession"),
    (0x0c528b, "JobLogin::processConsoleTicket"),
    (0x0c51a7, "JobLogin::processPostLogin"),
    (0x0c523f, "JobRequestConsoleTicket::initialize"),
    (0x0c5703, "JobRequestConsoleTicket::waitForFetchToken"),
]

for file_offset, label in targets:
    print(f"\n{label}")
    print(f"  file offset: 0x{file_offset:x}")

    found = False

    for s in sections:
        start = s["offset"]
        end = start + s["size"]

        if start <= file_offset < end:
            delta = file_offset - start
            virtual = s["addr"] + delta

            print(f"  section: #{s['index']} {section_name(s['name'])}")
            print(f"  delta:   0x{delta:x}")
            print(f"  address: 0x{virtual:08x}")

            found = True
            break

    if not found:
        print("  NOT FOUND IN SECTION TABLE")
