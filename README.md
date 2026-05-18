# Mini QA Tickets · Playwright Python BDD Automation

Proyecto de automatización diseñado para practicar:

- **Playwright con Python**
- **BDD con pytest-bdd**
- **Pruebas funcionales UI**
- **Pruebas combinadas API + UI usando Playwright APIRequestContext**
- **Reportes Allure con capturas de pantalla**
- Preparación para exploración con **Playwright MCP**
- Preparación para agentes de código con **Playwright CLI**

El proyecto está adaptado para la web **Mini QA Tickets**.

---

## 1. Requisitos

- Python 3.11+ recomendado
- Node.js 18+ si quieres usar Playwright MCP o Playwright CLI
- La app `mini-qa-tickets` ejecutándose en:

```text
http://localhost:3000
```

---

## 2. Crear entorno virtual e instalar dependencias

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m playwright install chromium
```

### Linux/macOS

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m playwright install chromium
```

---

## 3. Configuración

Copia `.env.example` a `.env`:

```powershell
Copy-Item .env.example .env
```

o:

```bash
cp .env.example .env
```

Por defecto:

```env
BASE_URL=http://localhost:3000
HEADLESS=true
```

Para ver el navegador:

```env
HEADLESS=false
```

---

## 4. Ejecutar los tests

```bash
pytest
```

También puedes ejecutar por marcas:

```bash
pytest -m ui
pytest -m api_ui
```

---

## 5. Generar resultados Allure

Los tests ya están configurados para guardar resultados en:

```text
reports/allure-results
```

Para generar y abrir el reporte, necesitas tener **Allure CLI** instalado:

```bash
allure serve reports/allure-results
```

o generar HTML estático:

```bash
allure generate reports/allure-results --clean -o reports/allure-report
```

---

## 6. Escenarios incluidos

### Scenario 1 · Filtrar tickets abiertos
- Navega al listado.
- Selecciona `Open`.
- Verifica que todos los tickets visibles están abiertos.

### Scenario 2 · Crear ticket desde la UI
- Abre el formulario.
- Rellena los datos.
- Crea el ticket.
- Valida el mensaje de éxito.
- Comprueba por API que existe.
- Lo elimina al final mediante API.

### Scenario 3 · Crear por API, borrar desde UI y validar por API
- Crea un ticket con `POST /api/tickets`.
- Lo localiza desde la UI.
- Pulsa el botón `Delete`.
- Comprueba el mensaje de borrado.
- Verifica con `GET /api/tickets/:id` que devuelve `404`.

---

## 7. Capturas en Allure

El proyecto adjunta:

- Capturas al final de cada escenario.
- Capturas automáticas cuando un test falla.
- Capturas específicas en puntos relevantes del flujo.

---

## 8. Estructura

```text
mini-qa-tickets-playwright-python/
├── AGENTS.md
├── README.md
├── requirements.txt
├── pytest.ini
├── .env.example
├── package.json
├── docs/
│   ├── playwright-mcp.md
│   └── playwright-cli-ai.md
├── features/
│   └── tickets.feature
├── pages/
│   ├── new_ticket_page.py
│   └── tickets_page.py
├── tests/
│   └── step_defs/
│       └── test_tickets_steps.py
└── utils/
    ├── api_client.py
    ├── artifacts.py
    └── data_factory.py
```

---

## 9. Notas de diseño

- Se usan `data-testid` del sitio Mini QA Tickets para crear localizadores estables.
- Se usa Page Object ligero para mantener los steps BDD legibles.
- La API se consume con **Playwright**, no con `requests`.
- Los datos de tickets se crean con títulos únicos para reducir colisiones.
