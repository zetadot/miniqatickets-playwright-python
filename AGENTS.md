# AGENTS.md

## Project intent

This repository automates the **Mini QA Tickets** training web app.

Primary goal:
- Practice Playwright UI automation with Python
- Practice API preparation and assertions with Playwright `APIRequestContext`
- Keep scenarios readable in BDD form

## Application under test

Default base URL:

```text
http://localhost:3000
```

Primary routes:
- `/tickets.html`
- `/new-ticket.html`

Primary API routes:
- `GET /api/tickets`
- `GET /api/tickets/:id`
- `POST /api/tickets`
- `DELETE /api/tickets/:id`

## Locator strategy

Prefer stable `data-testid` attributes already present in the app.

Examples:
- `ticket-search`
- `status-filter`
- `ticket-list`
- `ticket-card`
- `title-input`
- `project-input`
- `priority-select`
- `assignee-select`
- `description-input`
- `submit-ticket`
- `form-message`
- `ticket-feedback`
- `delete-ticket-<id>`

Avoid brittle XPath unless strictly necessary.

## Test-data rule

When creating tickets:
- Generate unique titles.
- Clean up tickets created by tests whenever possible.

## Playwright MCP

When using MCP, explore the live app at `http://localhost:3000` and prefer accessible roles and visible text first, then inspect `data-testid` only if needed.

## Playwright CLI for coding agents

When using `playwright-cli`, open the app first, inspect the page snapshot, and use element references returned by the CLI. Use the project tests as the source of truth for intended flows.
