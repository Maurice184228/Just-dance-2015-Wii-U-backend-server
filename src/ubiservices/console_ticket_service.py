from __future__ import annotations

from dataclasses import dataclass
from secrets import token_urlsafe


@dataclass
class ConsoleTicket:
    token_wiiu: str
    ticket: str
    principal_id_wiiu: str
    account_id_wiiu: str


class ConsoleTicketService:
    def __init__(self) -> None:
        self._tickets: dict[str, ConsoleTicket] = {}

    def get_or_create(
        self,
        auth_key: str,
        *,
        user_id: str,
    ) -> ConsoleTicket:
        existing = self._tickets.get(auth_key)

        if existing is not None:
            return existing

        ticket = ConsoleTicket(
            token_wiiu=auth_key.removeprefix("wiiu t="),
            ticket=token_urlsafe(32),
            principal_id_wiiu=user_id,
            account_id_wiiu=user_id,
        )

        self._tickets[auth_key] = ticket
        return ticket