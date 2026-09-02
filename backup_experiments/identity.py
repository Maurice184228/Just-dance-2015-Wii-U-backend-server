from __future__ import annotations

import hashlib
from uuid import UUID


def stable_uuid_from_authorization(
    authorization: str,
    namespace: str,
) -> str:
    """
    Generate a deterministic UUID-like identity from the Wii U
    authorization credential.

    The credential itself is never returned or logged.
    """

    material = f"{namespace}:{authorization}".encode("utf-8")

    digest = hashlib.sha256(material).digest()

    value = bytearray(digest[:16])

    # Make this a UUID version 4 / RFC 4122 variant.
    value[6] = (value[6] & 0x0F) | 0x40
    value[8] = (value[8] & 0x3F) | 0x80

    return str(UUID(bytes=bytes(value)))