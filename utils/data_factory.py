from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4


def unique_ticket_payload(prefix: str = "BDD ticket") -> dict[str, object]:
    token = uuid4().hex[:8]
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    return {
        "title": f"{prefix} {timestamp}-{token}",
        "description": "Ticket generated automatically by the Playwright Python BDD practice suite.",
        "status": "Open",
        "priority": "High",
        "project": "Mini QA Tickets Automation",
        "assigneeId": 1,
    }
