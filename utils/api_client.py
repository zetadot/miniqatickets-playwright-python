from __future__ import annotations

from dataclasses import dataclass

from playwright.sync_api import APIRequestContext


@dataclass(frozen=True)
class TicketRecord:
    id: int
    title: str
    raw: dict[str, object]


def create_ticket(api_request: APIRequestContext, payload: dict[str, object]) -> TicketRecord:
    response = api_request.post("/api/tickets", data=payload)
    if response.status != 201:
        raise AssertionError(f"Expected 201 creating ticket, got {response.status}: {response.text()}")
    body = response.json()
    return TicketRecord(id=int(body["id"]), title=str(body["title"]), raw=body)


def get_ticket_response(api_request: APIRequestContext, ticket_id: int):
    return api_request.get(f"/api/tickets/{ticket_id}")


def delete_ticket_if_present(api_request: APIRequestContext, ticket_id: int) -> None:
    response = api_request.delete(f"/api/tickets/{ticket_id}")
    if response.status not in {204, 404}:
        raise AssertionError(f"Unexpected delete status for ticket {ticket_id}: {response.status}")
