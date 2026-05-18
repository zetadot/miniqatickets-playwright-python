param(
    [Parameter(Mandatory = $true, Position = 0)]
    [string]$Task
)

$ErrorActionPreference = "Stop"

$VenvPython = ".\.venv\Scripts\python.exe"

$Tasks = @{

    "install" = {
        Write-Host "Creating virtual environment if it does not exist..."

        if (-not (Test-Path ".venv")) {
            python -m venv .venv
        }

        Write-Host "Upgrading pip..."
        & $VenvPython -m pip install --upgrade pip

        if ($LASTEXITCODE -ne 0) {
            throw "pip upgrade failed with exit code $LASTEXITCODE"
        }

        Write-Host "Installing project dependencies..."
        & $VenvPython -m pip install -r requirements.txt

        if ($LASTEXITCODE -ne 0) {
            throw "Dependency installation failed with exit code $LASTEXITCODE"
        }

        Write-Host "Installing Playwright Chromium browser..."
        & $VenvPython -m playwright install chromium

        if ($LASTEXITCODE -ne 0) {
            throw "Playwright browser installation failed with exit code $LASTEXITCODE"
        }
    }

    "install_chromium" = {
        Write-Host "Installing Playwright Chromium browser..."
        & $VenvPython -m playwright install chromium

        if ($LASTEXITCODE -ne 0) {
            throw "Playwright browser installation failed with exit code $LASTEXITCODE"
        }
    }

    "test" = {
        Write-Host "Running Playwright BDD tests..."
        & $VenvPython -m pytest

        if ($LASTEXITCODE -ne 0) {
            throw "Tests failed with exit code $LASTEXITCODE"
        }
    }

    "test-ui" = {
        Write-Host "Running UI tests..."
        & $VenvPython -m pytest -m ui

        if ($LASTEXITCODE -ne 0) {
            throw "UI tests failed with exit code $LASTEXITCODE"
        }
    }

    "test-api-ui" = {
        Write-Host "Running API + UI tests..."
        & $VenvPython -m pytest -m api_ui

        if ($LASTEXITCODE -ne 0) {
            throw "API + UI tests failed with exit code $LASTEXITCODE"
        }
    }

    "report" = {
        Write-Host "Opening Allure report..."
        allure serve reports/allure-results

        if ($LASTEXITCODE -ne 0) {
            throw "Allure report failed with exit code $LASTEXITCODE"
        }
    }

    "debug" = {
        Write-Host "Running tests in debug mode..."
        & $VenvPython -m debugpy --listen 5678 --wait-for-client -m pytest -m ui

        if ($LASTEXITCODE -ne 0) {
            throw "Debug tests failed with exit code $LASTEXITCODE"
        }
    }

    "all" = {
        Write-Host "Running full workflow..."
        & $Tasks["install"]
        & $Tasks["test"]
    }

    "allure" = {
        Write-Host "Opening Allure report..."
        & allure serve reports/allure-results
    }
}

if (-not $Tasks.ContainsKey($Task)) {
    Write-Host "Tarea no reconocida: $Task"
    Write-Host ""
    Write-Host "Tareas disponibles:"
    $Tasks.Keys | Sort-Object | ForEach-Object {
        Write-Host "  - $_"
    }
    exit 1
}

try {
    & $Tasks[$Task]
}
catch {
    Write-Error "La tarea '$Task' ha fallado: $($_.Exception.Message)"
    exit 1
}