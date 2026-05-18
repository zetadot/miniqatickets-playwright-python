Feature: Ticket management in Mini QA Tickets
  As a QA automation engineer
  I want to exercise both UI and API flows
  So that I can practice realistic Playwright automation patterns

  @ui
  Scenario: Filter open tickets from the ticket list
    Given I open the tickets page
    When I filter tickets by status "Open"
    Then every visible ticket should have status "Open"

  @ui
  Scenario: Create a ticket from the UI and verify it through the API
    Given I open the new ticket page
    When I create a unique ticket from the UI
    Then the UI should confirm the ticket was created
    And the created ticket should exist through the API

  @api_ui
  Scenario: Create a ticket through the API and delete it from the UI
    Given a unique ticket exists through the API
    When I search for that ticket in the tickets page
    And I delete that ticket from the list
    Then the UI should confirm the ticket was deleted
    And the deleted ticket should not exist through the API
