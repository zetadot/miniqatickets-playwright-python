from __future__ import annotations

from playwright.sync_api import Locator, Page, expect


class TicketsPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.search_input = page.get_by_test_id("ticket-search")
        self.status_filter = page.get_by_test_id("status-filter")
        self.ticket_cards = page.get_by_test_id("ticket-card")
        self.ticket_feedback = page.get_by_test_id("ticket-feedback")

    def open(self) -> None:
        self.page.goto("/tickets.html")
        expect(self.page.get_by_role("heading", name="Tickets")).to_be_visible()

    def filter_by_status(self, status: str) -> None:
        self.status_filter.select_option(label=status)

    def search(self, text: str) -> None:
        self.search_input.fill(text)

    def visible_statuses(self) -> list[str]:
        return self.page.get_by_test_id("ticket-status").all_text_contents()

    def expect_ticket_with_title(self, title: str) -> Locator:
        matching_card = self.ticket_cards.filter(has_text=title)
        expect(matching_card).to_have_count(1)
        return matching_card

    def delete_ticket(self, ticket_id: int) -> None:
        self.page.get_by_test_id(f"delete-ticket-{ticket_id}").click()

    def expect_delete_feedback(self, ticket_id: int) -> None:
        expect(self.ticket_feedback).to_contain_text(f"Ticket {ticket_id} deleted successfully.")
