from __future__ import annotations

import re

from playwright.sync_api import Page, expect


class NewTicketPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.title_input = page.get_by_test_id("title-input")
        self.project_input = page.get_by_test_id("project-input")
        self.priority_select = page.get_by_test_id("priority-select")
        self.assignee_select = page.get_by_test_id("assignee-select")
        self.description_input = page.get_by_test_id("description-input")
        self.submit_button = page.get_by_test_id("submit-ticket")
        self.form_message = page.get_by_test_id("form-message")

    def open(self) -> None:
        self.page.goto("/new-ticket.html")
        expect(self.page.get_by_role("heading", name="Create a ticket")).to_be_visible()

    def create_ticket(
        self,
        *,
        title: str,
        project: str,
        priority: str,
        assignee_index: int,
        description: str,
    ) -> None:
        self.title_input.fill(title)
        self.project_input.fill(project)
        self.priority_select.select_option(label=priority)
        self.assignee_select.select_option(index=assignee_index)
        self.description_input.fill(description)
        self.submit_button.click()

    def created_ticket_id(self) -> int:
        expect(self.form_message).to_contain_text("created successfully.")
        message = self.form_message.inner_text()
        match = re.search(r"Ticket\s+(\d+)\s+created successfully\.", message)
        if not match:
            raise AssertionError(f"Unable to extract ticket id from success message: {message}")
        return int(match.group(1))
