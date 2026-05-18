from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import allure
import pytest
from playwright.sync_api import APIRequestContext, Page
from pytest_bdd import given, parsers, scenario, then, when

from pages.new_ticket_page import NewTicketPage
from pages.tickets_page import TicketsPage
from utils.api_client import TicketRecord, create_ticket, delete_ticket_if_present, get_ticket_response
from utils.artifacts import attach_page_screenshot
from utils.data_factory import unique_ticket_payload


@dataclass
class ScenarioState:
    payload: dict[str, object] | None = None
    ticket_id: int | None = None
    ticket_title: str | None = None


@pytest.fixture()
def state() -> ScenarioState:
    return ScenarioState()


@scenario("tickets.feature", "Filter open tickets from the ticket list")
def test_filter_open_tickets() -> None:
    pass


@scenario("tickets.feature", "Create a ticket from the UI and verify it through the API")
def test_create_ticket_from_ui() -> None:
    pass


@scenario("tickets.feature", "Create a ticket through the API and delete it from the UI")
def test_create_by_api_delete_from_ui() -> None:
    pass


@given("I open the tickets page")
def open_tickets_page(page: Page) -> None:
    with allure.step("Open the tickets page"):
        TicketsPage(page).open()
        attach_page_screenshot(page, "tickets-page-opened")


@when(parsers.parse('I filter tickets by status "{status}"'))
def filter_tickets_by_status(page: Page, status: str) -> None:
    with allure.step(f'Filter tickets by status "{status}"'):
        TicketsPage(page).filter_by_status(status)
        attach_page_screenshot(page, f"tickets-filtered-{status.lower().replace(' ', '-')}")


@then(parsers.parse('every visible ticket should have status "{expected_status}"'))
def assert_every_visible_ticket_has_status(page: Page, expected_status: str) -> None:
    with allure.step(f'Validate every visible ticket status equals "{expected_status}"'):
        statuses = TicketsPage(page).visible_statuses()
        assert statuses, "Expected at least one visible ticket after filtering."
        assert all(status == expected_status for status in statuses), statuses


@given("I open the new ticket page")
def open_new_ticket_page(page: Page) -> None:
    with allure.step("Open the new ticket page"):
        NewTicketPage(page).open()
        attach_page_screenshot(page, "new-ticket-page-opened")


@when("I create a unique ticket from the UI")
def create_unique_ticket_from_ui(page: Page, state: ScenarioState) -> None:
    with allure.step("Create a unique ticket from the UI"):
        payload = unique_ticket_payload(prefix="UI BDD ticket")
        state.payload = payload
        state.ticket_title = str(payload["title"])

        NewTicketPage(page).create_ticket(
            title=str(payload["title"]),
            project=str(payload["project"]),
            priority=str(payload["priority"]),
            assignee_index=1,
            description=str(payload["description"]),
        )
        attach_page_screenshot(page, "ticket-created-from-ui")


@then("the UI should confirm the ticket was created")
def assert_ui_ticket_created(page: Page, state: ScenarioState) -> None:
    with allure.step("Validate UI success message after ticket creation"):
        state.ticket_id = NewTicketPage(page).created_ticket_id()
        assert state.ticket_id is not None


@then("the created ticket should exist through the API")
def assert_created_ticket_exists_through_api(api_request: APIRequestContext, state: ScenarioState) -> None:
    assert state.ticket_id is not None, "The ticket id was not captured from the UI."
    try:
        with allure.step("GET created ticket through API"):
            response = get_ticket_response(api_request, state.ticket_id)
            assert response.status == 200, response.text()
            body = response.json()
            assert body["title"] == state.ticket_title
    finally:
        delete_ticket_if_present(api_request, state.ticket_id)


@given("a unique ticket exists through the API")
def unique_ticket_exists_through_api(api_request: APIRequestContext, state: ScenarioState) -> None:
    with allure.step("Create ticket through API"):
        payload = unique_ticket_payload(prefix="API BDD ticket")
        ticket: TicketRecord = create_ticket(api_request, payload)
        state.payload = payload
        state.ticket_id = ticket.id
        state.ticket_title = ticket.title


@when("I search for that ticket in the tickets page")
def search_ticket_in_ui(page: Page, state: ScenarioState) -> None:
    assert state.ticket_title is not None
    with allure.step("Search created API ticket from the UI"):
        tickets_page = TicketsPage(page)
        tickets_page.open()
        tickets_page.search(state.ticket_title)
        tickets_page.expect_ticket_with_title(state.ticket_title)
        attach_page_screenshot(page, "api-created-ticket-visible-in-ui")


@when("I delete that ticket from the list")
def delete_that_ticket_from_list(page: Page, state: ScenarioState) -> None:
    assert state.ticket_id is not None
    with allure.step("Delete the API-created ticket from the UI"):
        tickets_page = TicketsPage(page)
        tickets_page.delete_ticket(state.ticket_id)
        attach_page_screenshot(page, "ticket-deleted-from-ui")


@then("the UI should confirm the ticket was deleted")
def assert_ui_ticket_deleted(page: Page, state: ScenarioState) -> None:
    assert state.ticket_id is not None
    with allure.step("Validate UI delete confirmation"):
        TicketsPage(page).expect_delete_feedback(state.ticket_id)


@then("the deleted ticket should not exist through the API")
def assert_deleted_ticket_not_found(api_request: APIRequestContext, state: ScenarioState) -> None:
    assert state.ticket_id is not None
    with allure.step("GET deleted ticket and expect 404"):
        response = get_ticket_response(api_request, state.ticket_id)
        assert response.status == 404, response.text()
