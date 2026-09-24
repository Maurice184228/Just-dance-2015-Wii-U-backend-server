from pathlib import Path

from capstone import (
    Cs,
    CS_ARCH_PPC,
    CS_MODE_BIG_ENDIAN,
    CS_MODE_32,
)

RPX = Path.home() / "Downloads" / "decompressed_output.rpx"

FILE_OFFSET = 0x002B4D40
SIZE = 0x0313230C
VIRTUAL_ADDRESS = 0x02000020

data = RPX.read_bytes()

end = FILE_OFFSET + SIZE

if end > len(data):
    raise ValueError(
        f"Section exceeds RPX size: 0x{end:x} > 0x{len(data):x}"
    )

code = data[FILE_OFFSET:end]

md = Cs(
    CS_ARCH_PPC,
    CS_MODE_BIG_ENDIAN | CS_MODE_32,
)

print("RPX PowerPC disassembly test")
print("============================")
print(f"RPX    : {RPX}")
print(f"Offset : 0x{FILE_OFFSET:08x}")
print(f"Size   : 0x{SIZE:08x}")
print(f"VAddr  : 0x{VIRTUAL_ADDRESS:08x}")
print()

decoded = 0

for insn in md.disasm(code, VIRTUAL_ADDRESS):
    decoded += 1

    print(
        f"0x{insn.address:08x}: "
        f"{insn.mnemonic:8s} "
        f"{insn.op_str}"
    )

    if decoded >= 200:
        break

print()
print(f"Decoded instructions shown: {decoded}")
