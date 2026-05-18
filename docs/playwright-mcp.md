# Playwright MCP · Mini QA Tickets

Playwright MCP allows an AI assistant to interact with the browser through the Model Context Protocol.

## Prerequisites

- Node.js 18+
- An MCP-capable client such as VS Code, Cursor, Claude Desktop, Claude Code or similar

## Standard MCP configuration

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

## VS Code CLI installation example

```bash
code --add-mcp '{"name":"playwright","command":"npx","args":["@playwright/mcp@latest"]}'
```

## Prompt example for this app

```text
Open http://localhost:3000.
Go to Tickets.
Filter by Open status.
Tell me how many visible tickets remain and whether all visible statuses are Open.
```

## More exploration prompts

```text
Open http://localhost:3000/new-ticket.html and inspect which fields are required to create a ticket.
```

```text
Create a ticket from the UI with title "MCP exploratory ticket", project "AI Practice", priority High, assign it to the first available user and report the success message.
```
