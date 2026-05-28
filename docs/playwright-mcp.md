# Playwright MCP · Mini QA Tickets

Playwright MCP allows an AI assistant to interact with a real browser through the Model Context Protocol.

It gives the assistant browser automation tools such as navigation, snapshots, clicks, typing, screenshots and other browser actions. The assistant uses Playwright through structured accessibility snapshots, so it can understand the page without relying only on screenshots.

Use this guide when you want an AI coding agent to explore the Mini QA Tickets app and help you create, improve or debug Playwright Python tests.

---

## When to use Playwright MCP

Use Playwright MCP when you want the AI assistant to:

- Open the application in a real browser.
- Explore pages and user flows.
- Inspect accessible elements.
- Interact with buttons, inputs, filters and forms.
- Create exploratory notes before writing tests.
- Suggest stable Playwright locators.
- Compare the UI behavior with BDD scenarios.
- Help generate or improve Python tests with `pytest-playwright`.

For this repository, Playwright MCP is mainly useful for exploration and test design. The final tests should still be written in Python using `pytest-playwright`.

---

## Prerequisites

- Node.js 18+
- An MCP-capable client, for example:
  - VS Code with GitHub Copilot Agent Mode
  - Cursor
  - Windsurf
  - Claude Desktop
  - Claude Code
  - Similar MCP clients

---

## Standard MCP configuration

Most MCP clients support a configuration similar to this:

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest"]
    }
  }
}
```

This tells the MCP client to start the Playwright MCP server using `npx`.

---

## VS Code CLI installation example

You can add Playwright MCP to VS Code using the CLI:

```bash
code --add-mcp '{"name":"playwright","command":"npx","args":["@playwright/mcp@latest"]}'
```

After adding it, restart VS Code or reload the window if the MCP server is not detected immediately.

In VS Code, you can also manage MCP servers from the UI if your version supports MCP server management.

---

## Claude Code installation example

For Claude Code, you can add the server with:

```bash
claude mcp add playwright npx @playwright/mcp@latest
```

---

## How to verify that MCP is being used

Ask the assistant to open the app and inspect the page.

Example prompt:

```text
Use Playwright MCP to open http://localhost:3000.
Inspect the page with an accessibility snapshot.
Tell me what main buttons, links and forms are visible.
```

If MCP is working, the assistant should use browser tools such as:

```text
browser_navigate
browser_snapshot
browser_click
browser_type
browser_take_screenshot
```

The exact tool names may vary depending on the client.

If the assistant only reads files or runs terminal commands, it may not be using Playwright MCP.

---

## Start the Mini QA Tickets app first

Before asking the assistant to use MCP, make sure the application is running.

Example:

```bash
python -m http.server 3000
```

Or use the project task/script if the repository provides one.

Then open:

```text
http://localhost:3000
```

or directly:

```text
http://localhost:3000/tickets.html
```

---

## Basic exploration prompt

```text
Use Playwright MCP to open http://localhost:3000.

Go to Tickets.
Inspect the page with an accessibility snapshot.
Tell me which filters, buttons and ticket cards are visible.
Do not write code yet.
First summarize the available user actions.
```

---

## Prompt example for this app

```text
Use Playwright MCP to open http://localhost:3000.

Go to Tickets.
Filter by Open status.
Tell me how many visible tickets remain.
Check whether all visible tickets have status Open.

Do not write code yet.
First explain the observed behavior.
```

---

## Explore the new ticket page

```text
Use Playwright MCP to open http://localhost:3000/new-ticket.html.

Inspect which fields are required to create a ticket.
Identify the best Playwright locators for each field.
Prefer role, label, placeholder and visible text locators.
Do not use XPath unless there is no better option.
```

---

## Create a ticket from the UI

```text
Use Playwright MCP to open http://localhost:3000/new-ticket.html.

Create a ticket from the UI with:
- Title: MCP exploratory ticket
- Project: AI Practice
- Priority: High
- Assignee: the first available user

After submitting, report the success message and the final page state.
```

---

## Recommended prompt for generating a test

```text
Use Playwright MCP to explore the ticket creation flow.

Then create or update a Python test using pytest-playwright.

Rules:
- Do not invent selectors.
- Use the observed UI structure.
- Prefer get_by_role, get_by_label, get_by_placeholder and get_by_text.
- Avoid XPath and long CSS chains.
- Do not use temporary MCP element refs in the final test.
- Follow the existing repository structure.
- Compare the flow with features/tickets.feature before writing code.
```

---

## Good final locator examples in Python

Prefer locators like these:

```python
page.get_by_role("button", name="Create ticket").click()
page.get_by_label("Title").fill("MCP exploratory ticket")
page.get_by_label("Project").fill("AI Practice")
page.get_by_label("Priority").select_option("High")
page.get_by_role("button", name="Save").click()
```

If accessibility locators are not enough, use stable CSS selectors:

```python
page.locator("[data-testid='create-ticket-button']").click()
```

Avoid fragile selectors:

```python
page.locator("div:nth-child(3) > form > button").click()
```

or long XPath expressions.

---

## Important: MCP refs are only for exploration

During MCP exploration, the assistant may use temporary element references from snapshots.

Example:

```text
button "Create ticket" [ref=e12]
textbox "Title" [ref=e18]
```

The assistant may click or fill those references while exploring.

However, the final automated test should not contain refs such as `e12` or `e18`.

Bad final test:

```python
page.locator("e12").click()
```

Good final test:

```python
page.get_by_role("button", name="Create ticket").click()
```

---

## Working with dynamic or complex pages

For simple pages such as Mini QA Tickets, a normal snapshot is usually enough.

For complex applications such as Salesforce, ServiceNow, Jira or SAP, ask the assistant to limit exploration.

Useful prompt:

```text
The page may be large and dynamic.
Use Playwright MCP snapshots carefully.
Do not inspect the whole page repeatedly if the output is too large.
Focus on the visible form, modal, table or main section.
Wait until spinners or loading overlays disappear before interacting.
Use screenshots only when the visual layout is important.
```

This helps avoid noisy snapshots and reduces the chance of choosing unstable elements.

---

## Recommended workflow with Playwright MCP

1. Start the Mini QA Tickets app.
2. Ask the assistant to open the app with Playwright MCP.
3. Ask it to inspect the page before writing code.
4. Ask it to list the relevant user actions.
5. Ask it to compare the UI with `features/tickets.feature`.
6. Ask it to propose missing scenarios.
7. Ask it to generate or update Python tests.
8. Run the tests with pytest.
9. Ask the assistant to debug failures using MCP if needed.

---

## Suggested BDD comparison prompt

```text
Use Playwright MCP to explore http://localhost:3000/tickets.html.

Then read features/tickets.feature.
Compare the real UI behavior with the existing BDD scenarios.

Return:
1. Existing scenarios that match the UI.
2. Missing scenarios worth adding.
3. Any mismatch between the UI and the feature file.

Do not modify code yet.
```

---

## Debugging prompt

```text
A pytest-playwright test is failing.

Use Playwright MCP to reproduce the failing flow manually in the browser.
Compare the real UI with the current test selectors.
Explain which selector or expectation is wrong.
Then propose the smallest code change needed.
```

---

## MCP vs Playwright CLI for coding agents

Both can help AI agents explore a browser, but they work differently.

| Tool | Best use |
|---|---|
| Playwright MCP | Interactive browser control through MCP tools inside an AI client |
| Playwright CLI for agents | Command-based browser exploration from terminal |
| Playwright normal CLI | Running tests, codegen, reports and standard Playwright workflows |

Use MCP when the AI assistant is working inside VS Code, Cursor, Claude Desktop or another MCP client.

Use Playwright CLI for agents when the assistant works mainly through terminal commands.

Use normal Playwright commands for running your actual tests.

---

## MCP vs final automated tests

Playwright MCP is not the final test framework.

For this repository:

```text
MCP = exploration and assistance
pytest-playwright = final automated tests
```

Run tests with:

```bash
pytest tests/
```

or with headed browser:

```bash
pytest tests/ --headed
```

Do not use:

```bash
npx playwright test
```

unless the repository also has Playwright Test TypeScript tests.

---

## Security and safety notes

Only allow MCP to interact with trusted local or test environments.

Recommended:

- Use local apps such as `localhost`.
- Avoid using production systems.
- Avoid entering real credentials.
- Use test users and test data.
- Review generated code before committing.
- Do not let the assistant perform destructive actions unless explicitly intended.

For enterprise apps such as Salesforce, prefer sandbox or QA environments.

---

## Useful prompts

### Inspect the current page

```text
Use Playwright MCP to inspect the current page.
List the visible headings, buttons, links, inputs and forms.
Suggest stable Playwright locators for the main actions.
```

### Explore filters

```text
Use Playwright MCP to open http://localhost:3000/tickets.html.
Test each ticket filter one by one.
Report what changes in the visible ticket list.
```

### Explore search

```text
Use Playwright MCP to open http://localhost:3000/tickets.html.
Use the search field to search for "login".
Report which ticket cards remain visible.
```

### Create scenario proposal

```text
Use Playwright MCP to explore the ticket list and ticket creation flow.
Propose 3 BDD scenarios that would add useful coverage.
Do not write code yet.
```

### Generate Python test

```text
Use Playwright MCP to explore the ticket creation flow.
Then generate a pytest-playwright test following the existing project structure.
Use stable locators and avoid XPath.
```

---

## Quick summary

```text
Use Playwright MCP to let the assistant explore the app in a real browser.
Use snapshots to understand the UI.
Use MCP refs only during exploration.
Use stable Playwright locators in the final Python tests.
Use pytest-playwright to run the final tests.
```
