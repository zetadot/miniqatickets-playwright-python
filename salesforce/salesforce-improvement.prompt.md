Read `salesforce/get-sf-token.ps1` first. This PowerShell script connects to a Salesforce org via API using a JWT token and returns useful session data, including a `frontdoor.jsp` URL for a specific user.

Create a new feature file and a new step definition file that replicate this logic.

The flow should be:

1. Get the Salesforce access token using the same JWT/API logic.
2. Generate or retrieve the `frontdoor.jsp` URL for the target user.
3. Open that URL with Playwright.
4. Impersonate the user by clicking the “Login” / “Login As” action.
5. Navigate to Cases.
6. Open one Case record.

Use Playwright CLI/MCP to inspect the UI and choose reliable locators.
Keep the implementation clean, reusable, and aligned with the existing project structure.