# SXM Test Planner Prototype

A professional simulator-first prototype that turns existing Robot Framework tests into a visual test catalogue and click-to-run workflow.

## What the prototype proves

```text
Robot repository
      ↓
Catalogue scanner
      ↓
List / Grid UI
      ↓
Select test(s)
      ↓
Create execution cycle
      ↓
Safe runner adapter
      ↓
PASS / FAIL results and artifacts
```

The Robot scripts remain the source of test logic. The web application handles discovery, selection, safe execution orchestration, status, history, and result presentation.

## Prototype boundaries

- Simulator and demo data only by default.
- No real DUT, SAT emulator, proxy, Jumpstarter, SSH, ADB, relay, ignition, TestRail publishing, or OpenShift integration.
- No free-text shell commands.
- The runner accepts only catalogue IDs discovered below an allow-listed repository root.
- Replace adapters under `services/api/app/adapters/` when approved production integrations become available.

## Architecture

```text
apps/web (Next.js App Router + TypeScript)
        ↓ REST / polling
services/api (FastAPI)
        ├── CatalogueService
        │     ├── DemoCatalogueAdapter
        │     └── RobotCatalogueAdapter
        ├── PlannerService
        ├── RunnerAdapter
        │     ├── SimulatedRunnerAdapter (default)
        │     └── LocalRobotRunnerAdapter (opt-in)
        ├── ResultAdapter
        │     └── Robot output.xml parser
        └── SQLite run history
```

## UI pages

- `/` dashboard
- `/catalog` list/grid test catalogue with search and filters
- `/runs/new` cycle builder
- `/runs` run history
- `/runs/[id]` live status and per-test results
- `/targets` execution target capability view
- `/architecture` system model and prototype boundaries

## Quick start on Windows

### Prerequisites

- Node.js 24 or later
- Python 3.13
- `uv`

### One-command setup

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\scripts\setup.ps1
```

### Run both services

```powershell
.\scripts\dev.ps1
```

Open:

- Web: `http://localhost:3000`
- API: `http://localhost:8000`
- OpenAPI: `http://localhost:8000/docs`

The default runner is simulated and completes runs locally without hardware.

## Connect the current learning repository

Set the Robot repository path before starting the API:

```powershell
$env:ROBOT_REPO_ROOT = 'C:\Users\shanmukhacm\Desktop\beacon\sxm-ivi-test-automation-learning'
$env:CATALOG_MODE = 'robot'
```

The catalogue adapter discovers `.robot` files and tests below the configured root. Execution remains simulated unless explicitly changed.

## Optional local Robot execution

Use only with the simulator-safe learning repository:

```powershell
$env:RUNNER_MODE = 'robot'
```

The local runner:

- validates every test ID against the current catalogue
- allows only paths below `ROBOT_REPO_ROOT`
- invokes Robot with an argument array, not a shell command
- creates one result directory per run
- records the Git revision when available
- parses `output.xml` with the Robot Framework API

Do not enable the Robot runner against real hardware until the approved framework and authorization model are available.

## Replace demo integrations later

| Prototype adapter | Approved replacement later |
|---|---|
| `DemoCatalogueAdapter` | Official repository catalogue scanner |
| `SimulatedRunnerAdapter` | Authorized job/runner service |
| `LocalTargetAdapter` | Approved DUT/bench inventory |
| Local SQLite | Approved team database |
| Local artifact paths | JFrog or approved artifact store |
| No authentication | Company SSO/RBAC |
| No TestRail publishing | Approved TestRail reporter |

## Quality checks

### Backend

```powershell
cd services/api
uv run ruff check
uv run pytest -q
```

### Frontend

```powershell
cd apps/web
npm run lint
npm run build
```
