# High-level architecture

## Core rule

The web application never owns product test logic. Robot suites and resources remain the executable source of truth.

## Request flow

```text
Browser
  │
  ├─ GET /api/catalog
  │      └─ Catalogue adapter → approved Robot repository
  │
  ├─ POST /api/runs
  │      └─ Planner validates tests + target compatibility
  │
  └─ GET /api/runs/{id}
         └─ Run state + parsed Robot results + artifact links

Planner
  │
  ├─ Capability matcher
  ├─ Safe allow-list validation
  ├─ Runner adapter
  └─ SQLite history

Runner adapter
  │
  ├─ Simulated runner for prototype
  └─ Local Robot runner for simulator-only integration
```

## Domain objects

### TestDefinition
- stable catalogue ID
- exact Robot test name
- source suite path
- product area
- tags and optional C-tag
- required driver configuration
- required capabilities
- enabled/readiness state

### Target
- target ID and display name
- availability state
- capabilities
- target type

### Run
- selected tests
- target
- source revision
- queued/running/completed timestamps
- overall status
- individual test results
- artifacts

## Status model

```text
DRAFT → QUEUED → PREPARING → RUNNING → COLLECTING_RESULTS
                                              ↓
                          PASSED / FAILED / BLOCKED / CANCELLED
                                              ↓
                                          COMPLETED
```

## Integration seam

The backend routes depend on service protocols, not on simulator implementation details. Replace adapter classes without changing UI contracts.
