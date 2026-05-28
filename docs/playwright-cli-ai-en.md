# Playwright CLI for Coding Agents · Mini QA Tickets

Playwright CLI allows AI coding agents such as GitHub Copilot, Claude Code, Cursor or similar tools to explore a web application using concise browser commands.

It is useful for:

- Navigating the application.
- Inspecting accessible snapshots.
- Identifying interactive elements.
- Proposing or correcting tests.
- Comparing the real application flow with BDD scenarios.

---

## Prerequisites

- Node.js 18+
- A compatible AI coding agent:
  - GitHub Copilot
  - Claude Code
  - Cursor
  - Similar tools

---

## Installation

Global installation:

```bash
npm install -g @playwright/cli@latest
playwright-cli --help
```

Alternative usage with `npx`:

```bash
npx playwright-cli --help
```

---

## Install agent skills

Playwright CLI can install agent skills/instructions so the coding agent understands how to use the tool better.

```bash
playwright-cli install --skills
```

---

## Open the application

To open the application manually:

```bash
playwright-cli open http://localhost:3000/tickets.html --headed
```

Or using `npx`:

```bash
npx playwright-cli open http://localhost:3000/tickets.html --headed
```

---

## Inspect the page with snapshot

The `snapshot` command returns the accessible tree of the current page.

```bash
playwright-cli snapshot
```

Example output:

```text
- heading "Mini QA Tickets"
- button "Create ticket" [ref=e3]
- combobox "Status" [ref=e5]
- textbox "Search" [ref=e7]
```

References such as `e3`, `e5` or `e7` are temporary element references that can be used during exploration.

Example:

```bash
playwright-cli click e3
playwright-cli fill e7 "login"
```

Important: snapshot references are temporary. They should not be used in the final automated test.

In final tests, prefer stable locators such as:

```python
page.get_by_role("button", name="Create ticket").click()
page.get_by_label("Search").fill("login")
```

---

## Improve snapshots in large or dynamic applications

In complex applications such as Salesforce, ServiceNow, SAP, Jira or large enterprise portals, a full `snapshot` can be too large or difficult for the agent to interpret.

The snapshot is reliable regarding the accessibility tree that Playwright can see, but it may not fully represent the visual complexity of the page.

```text
The snapshot shows what Playwright can read from the accessibility tree.
It does not always represent the complete visual layout of the page.
```

This is especially important in applications with:

- Dynamic components.
- Shadow DOM.
- Custom widgets.
- Modals.
- Tabs.
- Side panels.
- Lazy-loaded content.
- Spinners or loading states.
- Large forms with repeated labels.
- Tables with many rows and columns.

---

## Do not edit snapshots manually

Playwright CLI may store snapshots as `.yml` files, for example:

```text
.playwright-cli/page-2026-...yml
```

However, editing that file does not improve the real page.

It is only a representation of what Playwright saw at that moment.

Do not try to fix selectors by editing the snapshot. Instead, improve the exploration strategy.

---

## Limit the snapshot scope

For large pages, avoid taking a full-page snapshot repeatedly if it is not necessary.

Instead, take a snapshot of a specific area.

Example using a CSS selector:

```bash
playwright-cli snapshot "#main"
```

Example using a previous snapshot reference:

```bash
playwright-cli snapshot e34
```

Example limiting the depth:

```bash
playwright-cli snapshot --depth=4
```

This helps the agent focus only on the useful part of the page.

---

## Recommended strategy for dynamic pages

Use this order:

```text
1. Wait until the page is stable.
2. Take an initial snapshot.
3. Identify the main section, form, modal, tab or table.
4. Take a smaller snapshot of that area.
5. Interact using snapshot refs only during exploration.
6. Generate the final test using stable Playwright locators.
```

For example:

```bash
playwright-cli snapshot
playwright-cli snapshot "#content"
playwright-cli snapshot --depth=4
```

If the page has a modal:

```bash
playwright-cli snapshot
playwright-cli snapshot "[role='dialog']"
```

If the page has a data table:

```bash
playwright-cli snapshot
playwright-cli snapshot "table"
```

If the page has a main application area:

```bash
playwright-cli snapshot "main"
```

---

## Combine snapshot with screenshot

In some enterprise applications, not everything is clearly exposed in the accessibility tree.

For example:

- Icons without accessible names.
- Complex menus.
- Canvas elements.
- Charts.
- Custom dropdowns.
- Visual-only validation messages.
- Hidden side panels.

In these cases, combine:

```bash
playwright-cli snapshot
playwright-cli screenshot
```

Use `snapshot` to interact with elements.

Use `screenshot` to understand the visual layout.

---

## Wait before taking snapshots

Dynamic applications often need extra time after navigation, clicks or form actions.

Before taking a snapshot, make sure the UI is stable.

For example, after opening a page or clicking a button, ask the agent to wait until:

- The spinner disappears.
- The modal is visible.
- The table has loaded.
- The expected heading appears.
- The button becomes enabled.
- The URL changes.
- The network activity finishes.

Useful instruction for the agent:

```text
After each navigation or click, wait until the page is stable before taking the next snapshot.
Do not inspect the page while a spinner, loading overlay or skeleton screen is still visible.
```

---

## Use refs only for exploration

Snapshot refs such as `e1`, `e2`, `e3` are useful for the agent while exploring:

```bash
playwright-cli click e45
playwright-cli fill e52 "Test account"
```

But they should not be used in the final automated test.

Bad final test:

```python
page.locator("e45").click()
```

Good final test:

```python
page.get_by_role("button", name="Save").click()
```

or:

```python
page.get_by_label("Account Name").fill("Test account")
```

---

## Prefer stable locators in final tests

For the final Python test, prefer:

```python
page.get_by_role("button", name="Save")
page.get_by_label("Account Name")
page.get_by_text("Open")
page.get_by_placeholder("Search")
```

If accessibility locators are not enough, use a stable CSS selector:

```python
page.locator("[data-testid='save-button']")
```

Avoid fragile selectors such as:

```python
page.locator("div:nth-child(4) > span > button")
```

or long XPath expressions.

---

## Recommended order for Salesforce-like applications

For complex applications such as Salesforce Lightning, use this priority:

```text
1. Snapshot of the current page.
2. Snapshot limited to a section, form, modal, tab or table.
3. Locator by role, label, placeholder or visible text.
4. Screenshot to understand the visual layout.
5. Stable CSS selector if accessibility is not enough.
6. Coordinate-based interaction only as a last resort.
```

Coordinate-based actions are less maintainable and should only be used when the element is not available through the accessibility tree.

Example:

```bash
playwright-cli screenshot
playwright-cli mousemove 850 45
playwright-cli mousedown
playwright-cli mouseup
```

Use this only for special cases such as canvas, maps or very custom widgets.

---

## Named sessions

To work with a specific session, define the `PLAYWRIGHT_CLI_SESSION` environment variable.

In PowerShell:

```powershell
$env:PLAYWRIGHT_CLI_SESSION="mini-qa-tickets"
npx playwright-cli open http://localhost:3000/tickets.html
npx playwright-cli list
```

This makes the commands use the `mini-qa-tickets` session.

If you do not define the environment variable, you can specify the session with `-s`:

```bash
playwright-cli -s=mini-qa-tickets open http://localhost:3000/tickets.html
playwright-cli -s=mini-qa-tickets snapshot
```

---

## Persistent session

To keep cookies, localStorage and browser state between restarts:

```bash
playwright-cli open http://localhost:3000/tickets.html --persistent
```

This is useful when you need to preserve login state or browser configuration.

---

## List active sessions

To list active sessions:

```bash
playwright-cli list
```

Example:

```text
Active sessions:
-> mini-qa-tickets (http://localhost:3000/tickets.html)
   default (about:blank)
```

The arrow `->` indicates the active/default session.

---

## Open the visual dashboard

To open the Playwright CLI visual dashboard:

```bash
playwright-cli show
```

This is useful for viewing open sessions, URLs and browser state.

---

## Useful commands

| Action | Command |
|---|---|
| Open a URL | `playwright-cli open http://localhost:3000/tickets.html` |
| Open with visible browser | `playwright-cli open http://localhost:3000/tickets.html --headed` |
| Get accessible snapshot | `playwright-cli snapshot` |
| Limit snapshot depth | `playwright-cli snapshot --depth=4` |
| Snapshot a section | `playwright-cli snapshot "#main"` |
| Click a reference | `playwright-cli click e3` |
| Fill text | `playwright-cli fill e5 "text"` |
| Take screenshot | `playwright-cli screenshot` |
| List sessions | `playwright-cli list` |
| Open dashboard | `playwright-cli show` |
| Use a specific session | `playwright-cli -s=mini-qa-tickets snapshot` |
| Close a session | `playwright-cli -s=mini-qa-tickets close` |

---

## Prompt example for a coding agent

```text
Use playwright-cli to open http://localhost:3000/tickets.html.

Explore the Mini QA Tickets application using snapshots.
Filter tickets by Open status.
Inspect the visible ticket cards.
Compare the behavior with the BDD scenarios in features/tickets.feature.

Do not invent selectors.
Prefer accessible locators such as get_by_role, get_by_label and get_by_text.
Before writing code, propose the test scenarios you would automate.
```

---

## Prompt example for complex applications

```text
Use playwright-cli to explore the application.

The page may be large and dynamic, similar to Salesforce Lightning.
Do not take full snapshots repeatedly if the output is too large.
First identify the relevant section, heading, form, modal, tab or table.
Then take a limited snapshot of that area.

Wait until spinners, loading overlays or skeleton screens disappear before inspecting the page.

Use snapshot refs only for exploration.
Do not use refs like e1, e2 or e3 in the final test.

Generate the final test in Python with pytest-playwright.
Prefer get_by_role, get_by_label, get_by_placeholder and get_by_text.
Use stable CSS selectors only if accessibility locators are not enough.
Avoid XPath and long CSS chains.
```

---

## Suggested workflow for this repository

Recommended flow when using a coding agent:

1. Open the application with Playwright CLI.
2. Inspect the page using `snapshot`.
3. Explore the main user flows:
   - List tickets.
   - Filter by status.
   - Search tickets.
   - Create a ticket.
   - Validate visible ticket data.
4. Compare the real behavior with `features/tickets.feature`.
5. Propose new BDD scenarios.
6. Implement or update the Python tests using `pytest-playwright`.
7. Use stable locators in the final test code.

---

## Important notes

- `playwright-cli` is for agent-assisted exploration.
- The final automated tests should not depend on snapshot refs like `e1`, `e2`, `e3`.
- Prefer Playwright locators based on accessibility:

```python
page.get_by_role("button", name="Create ticket")
page.get_by_label("Status")
page.get_by_text("Open")
```

- For this repository, tests should be written in Python with `pytest-playwright`, not with `npx playwright test`.

Example:

```bash
pytest tests/
```

or:

```bash
pytest tests/ --headed
```

---

## Quick summary

```text
Do not edit snapshots manually.
Improve them by reducing scope, limiting depth and waiting for the UI to be stable.
Use screenshots when the visual layout matters.
Use refs only during exploration.
Use stable Playwright locators in the final test.
```

### Broser config

On the folder `.playwright` create the file `cli.config.json` with the following to make playwright cli to use specific browser, by example msedge:
```
{
  "browser": {
    "browserName": "chromium",
    "launchOptions": {
      "channel": "msedge"
    }
  }
}
```