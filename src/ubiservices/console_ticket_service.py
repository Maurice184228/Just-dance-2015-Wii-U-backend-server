from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ConsoleTicket:
    token_wiiu: str
    ticket: str
    principal_id_wiiu: str
    account_id_wiiu: str


class ConsoleTicketService:
    def __init__(self) -> None:
        self._tickets: dict[str, ConsoleTicket] = {}

    def get(self, auth_key: str) -> ConsoleTicket | None:
        return self._tickets.get(auth_key)

    def store(
        self,
        auth_key: str,
        *,
        token_wiiu: str,
        ticket: str,
        principal_id_wiiu: str,
        account_id_wiiu: str,
    ) -> ConsoleTicket:
        console_ticket = ConsoleTicket(
            token_wiiu=token_wiiu,
            ticket=ticket,
            principal_id_wiiu=principal_id_wiiu,
            account_id_wiiu=account_id_wiiu,
        )

        self._tickets[auth_key] = console_ticket
        return console_ticket