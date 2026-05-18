# Playwright CLI for coding agents · Mini QA Tickets

Playwright CLI is intended for coding agents that benefit from concise browser commands and installable skills.

## Prerequisites

- Node.js 18+
- A coding agent such as Claude Code, GitHub Copilot or similar

## Installation

Global:

```bash
npm install -g @playwright/cli@latest
playwright-cli --help
```

Alternative using `npx`:

```bash
npx playwright-cli --help
```

## Install skills

```bash
playwright-cli install --skills
```

## Manual walkthrough for the app

```bash
playwright-cli open http://localhost:3000/tickets.html --headed
```

Then inspect the snapshot and continue with commands based on returned element references.

## Prompt example for a coding agent

```text
Use playwright-cli to open http://localhost:3000/tickets.html.
Filter tickets by Open status.
Inspect the visible ticket cards and summarize whether the UI behaves as expected.
```

## Suggested use with this repository

Ask the coding agent to:
1. Explore the app with Playwright CLI.
2. Compare the flow with the BDD scenarios in `features/tickets.feature`.
3. Propose new automated scenarios before writing code.
