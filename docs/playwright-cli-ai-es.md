# Playwright CLI for Coding Agents · Mini QA Tickets

Playwright CLI permite que agentes de IA como GitHub Copilot, Claude Code, Cursor u otros exploren una aplicación web usando comandos de navegador simples y compactos.

Es útil para:

- Navegar la app.
- Obtener snapshots accesibles.
- Identificar elementos interactivos.
- Proponer o corregir tests.
- Comparar el flujo real con los escenarios BDD.

---

## Prerequisites

- Node.js 18+
- Un agente de IA compatible, por ejemplo:
  - GitHub Copilot
  - Claude Code
  - Cursor
  - similar

---

## Installation

Instalación global:

```bash
npm install -g @playwright/cli@latest
playwright-cli --help
```

Uso alternativo con `npx`:

```bash
npx playwright-cli --help
```

---

## Install agent skills

Playwright CLI puede instalar instrucciones o skills para que el agente entienda mejor cómo usar la herramienta.

```bash
playwright-cli install --skills
```

---

## Open the application

Para abrir la aplicación manualmente:

```bash
playwright-cli open http://localhost:3000/tickets.html --headed
```

O usando `npx`:

```bash
npx playwright-cli open http://localhost:3000/tickets.html --headed
```

---

## Inspect the page with snapshot

El comando `snapshot` devuelve el árbol accesible de la página. No genera una imagen; genera una representación textual de los elementos que Playwright puede leer.

```bash
playwright-cli snapshot
```

Ejemplo de resultado esperado:

```text
- heading "Mini QA Tickets"
- button "Create ticket" [ref=e3]
- combobox "Status" [ref=e5]
- textbox "Search" [ref=e7]
```

Las referencias como `e3`, `e5` o `e7` sirven para interactuar temporalmente con los elementos.

Ejemplo:

```bash
playwright-cli click e3
playwright-cli fill e7 "login"
```

Importante: las referencias del snapshot son temporales. No deberían usarse en el test final. En los tests es mejor usar locators estables como:

```python
page.get_by_role("button", name="Create ticket").click()
page.get_by_label("Search").fill("login")
```

---

## Improve snapshots in large or dynamic applications

En aplicaciones complejas como Salesforce, ServiceNow, SAP, Jira o portales empresariales grandes, un `snapshot` completo puede ser demasiado grande o difícil de interpretar para el agente.

El snapshot es fiable respecto al árbol accesible que Playwright puede ver, pero puede no representar toda la complejidad visual de la pantalla.

```text
The snapshot shows what Playwright can read from the accessibility tree.
It does not always represent the complete visual layout of the page.
```

Esto es especialmente importante en aplicaciones con:

- Componentes dinámicos.
- Shadow DOM.
- Widgets personalizados.
- Modales.
- Tabs.
- Paneles laterales.
- Contenido cargado bajo demanda.
- Spinners o estados de carga.
- Formularios grandes con muchas etiquetas repetidas.
- Tablas con muchas filas y columnas.

---

## Do not edit the snapshot manually

Playwright CLI puede guardar snapshots como archivos `.yml`, por ejemplo:

```text
.playwright-cli/page-2026-...yml
```

Pero editar ese archivo no mejora la página real ni los elementos reales. Es solo una representación de lo que Playwright vio en ese momento.

No intentes corregir selectores editando el snapshot. Es mejor mejorar la estrategia de exploración.

---

## Limit the snapshot scope

En páginas grandes, evita pedir siempre un snapshot completo. Es mejor hacer snapshot de una zona concreta.

Ejemplo usando un selector CSS:

```bash
playwright-cli snapshot "#main"
```

Ejemplo usando una referencia previa del snapshot:

```bash
playwright-cli snapshot e34
```

Ejemplo limitando profundidad:

```bash
playwright-cli snapshot --depth=4
```

Esto ayuda al agente a centrarse solo en la parte útil de la página.

Ejemplos habituales:

```bash
# Zona principal
playwright-cli snapshot "main"

# Modal visible
playwright-cli snapshot "[role='dialog']"

# Tabla de datos
playwright-cli snapshot "table"

# Contenedor específico
playwright-cli snapshot "#content"
```

---

## Recommended strategy for dynamic pages

Usa este orden en aplicaciones dinámicas:

```text
1. Esperar a que la página esté estable.
2. Sacar un snapshot inicial.
3. Identificar la sección principal, formulario, modal, tab o tabla.
4. Sacar un snapshot más pequeño de esa zona.
5. Usar refs solo durante la exploración.
6. Generar el test final con locators estables de Playwright.
```

Después de navegar, hacer click o enviar un formulario, pide al agente que espere antes de inspeccionar de nuevo.

Debe esperar hasta que:

- Desaparezca el spinner.
- El modal sea visible.
- La tabla haya cargado.
- Aparezca el heading esperado.
- El botón esté habilitado.
- Cambie la URL.
- La actividad de red se estabilice.

Prompt útil:

```text
After each navigation or click, wait until the page is stable before taking the next snapshot.
Do not inspect the page while a spinner, loading overlay or skeleton screen is still visible.
```

---

## Combine snapshot with screenshot

En algunas aplicaciones empresariales, no todo aparece claramente en el árbol accesible.

Por ejemplo:

- Iconos sin nombre accesible.
- Menús complejos.
- Elementos canvas.
- Gráficos.
- Dropdowns personalizados.
- Validaciones solo visuales.
- Paneles laterales ocultos.

En estos casos, combina:

```bash
playwright-cli snapshot
playwright-cli screenshot
```

Usa `snapshot` para interactuar con elementos. Usa `screenshot` para entender el layout visual.

---

## Vision mode and coordinates

Si un elemento no aparece en el árbol accesible, el agente puede apoyarse en una captura visual y usar coordenadas.

Ejemplo:

```bash
playwright-cli screenshot
playwright-cli mousemove 850 45
playwright-cli mousedown
playwright-cli mouseup
```

Esto debe ser el último recurso, porque las coordenadas son menos mantenibles. Pueden fallar si cambia la resolución, el zoom, el tamaño de ventana o el layout.

Úsalo solo para casos especiales como:

- Canvas.
- Mapas.
- Gráficos interactivos.
- Widgets muy personalizados.
- Elementos que no aparecen en el árbol accesible.

---

## Recommended order for Salesforce-like applications

Para aplicaciones tipo Salesforce Lightning, usa esta prioridad:

```text
1. Snapshot de la página actual.
2. Snapshot limitado a sección, formulario, modal, tab o tabla.
3. Locator por role, label, placeholder o texto visible.
4. Screenshot para entender el layout visual.
5. CSS estable si accessibility no es suficiente.
6. Coordenadas solo como último recurso.
```

Prompt útil para Copilot, Claude o Cursor:

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

## Use refs only for exploration

Las refs del snapshot son útiles para explorar:

```bash
playwright-cli click e45
playwright-cli fill e52 "Test account"
```

Pero no deben aparecer en el test final.

Mal ejemplo en test final:

```python
page.locator("e45").click()
```

Buen ejemplo en test final:

```python
page.get_by_role("button", name="Save").click()
page.get_by_label("Account Name").fill("Test account")
```

---

## Prefer stable locators in final tests

Para el test final en Python, prioriza:

```python
page.get_by_role("button", name="Save")
page.get_by_label("Account Name")
page.get_by_text("Open")
page.get_by_placeholder("Search")
```

Si los locators accesibles no son suficientes, usa un selector CSS estable:

```python
page.locator("[data-testid='save-button']")
```

Evita selectores frágiles:

```python
page.locator("div:nth-child(4) > span > button")
```

Y evita XPath largos siempre que sea posible.

---

## Named sessions

Para trabajar con una sesión concreta, puedes definir la variable `PLAYWRIGHT_CLI_SESSION`.

En PowerShell:

```powershell
$env:PLAYWRIGHT_CLI_SESSION="mini-qa-tickets"
npx playwright-cli open http://localhost:3000/tickets.html
npx playwright-cli list
```

Esto hace que los comandos usen la sesión llamada `mini-qa-tickets`.

Si no defines la variable de entorno, puedes indicar la sesión con `-s`:

```bash
playwright-cli -s=mini-qa-tickets open http://localhost:3000/tickets.html
playwright-cli -s=mini-qa-tickets snapshot
```

---

## Persistent session

Para mantener cookies, localStorage y estado del navegador entre reinicios:

```bash
playwright-cli open http://localhost:3000/tickets.html --persistent
```

Esto es útil si necesitas conservar login o configuración del navegador.

---

## List active sessions

Para ver las sesiones activas:

```bash
playwright-cli list
```

Ejemplo:

```text
Active sessions:
-> mini-qa-tickets (http://localhost:3000/tickets.html)
   default (about:blank)
```

La flecha `->` indica la sesión activa.

---

## Open the visual dashboard

Para abrir el dashboard visual de Playwright CLI:

```bash
playwright-cli show
```

Sirve para ver las sesiones abiertas, URLs y estado del navegador.

---

## Useful commands

| Acción | Comando |
|---|---|
| Abrir una URL | `playwright-cli open http://localhost:3000/tickets.html` |
| Abrir con navegador visible | `playwright-cli open http://localhost:3000/tickets.html --headed` |
| Obtener snapshot accesible | `playwright-cli snapshot` |
| Snapshot de una sección | `playwright-cli snapshot "#main"` |
| Snapshot por profundidad | `playwright-cli snapshot --depth=4` |
| Hacer screenshot | `playwright-cli screenshot` |
| Hacer click en una referencia | `playwright-cli click e3` |
| Escribir texto | `playwright-cli fill e5 "texto"` |
| Ver sesiones | `playwright-cli list` |
| Abrir dashboard | `playwright-cli show` |
| Usar sesión concreta | `playwright-cli -s=mini-qa-tickets snapshot` |
| Cerrar sesión | `playwright-cli -s=mini-qa-tickets close` |

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

## Suggested workflow for this repository

Recommended flow when using a coding agent:

1. Open the application with Playwright CLI.
2. Inspect the page using `snapshot`.
3. If the page is large, limit the snapshot to a section, modal, form or table.
4. Explore the main user flows:
   - List tickets.
   - Filter by status.
   - Search tickets.
   - Create a ticket.
   - Validate visible ticket data.
5. Compare the real behavior with `features/tickets.feature`.
6. Propose new BDD scenarios.
7. Implement or update the Python tests using `pytest-playwright`.
8. Use stable locators in the final test code.

---

## Important notes

- `playwright-cli` is for agent-assisted exploration.
- The final automated tests should not depend on snapshot refs like `e1`, `e2`, `e3`.
- Do not edit snapshots manually.
- Improve snapshots by reducing scope, limiting depth and waiting for the UI to be stable.
- Use screenshots when the visual layout matters.
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
