from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RDVOperation:
    code: int
    name: str
    description: str


OPERATIONS: dict[int, RDVOperation] = {
    0x0040: RDVOperation(
        code=0x0040,
        name="operation_0040",
        description="Observed in captured packet 593",
    ),
    0x0061: RDVOperation(
        code=0x0061,
        name="operation_0061",
        description="Observed request with captured 0x0091 response",
    ),
    0x0062: RDVOperation(
        code=0x0062,
        name="operation_0062",
        description="Observed in captured packet 600",
    ),
    0x0090: RDVOperation(
        code=0x0090,
        name="operation_0090",
        description="Observed in captured packet 594",
    ),
    0x0091: RDVOperation(
        code=0x0091,
        name="operation_0091",
        description="Observed response to operation 0x0061",
    ),
}


def get_operation(code: int) -> RDVOperation | None:
    return OPERATIONS.get(code)