# API contract

## Catalogue

- `GET /api/catalog`
- `GET /api/catalog/{test_id}`

## Targets

- `GET /api/targets`

## Runs

- `POST /api/runs`
- `GET /api/runs`
- `GET /api/runs/{run_id}`
- `POST /api/runs/{run_id}/cancel`

## Artifacts

- `GET /api/runs/{run_id}/artifacts/{artifact_name}`

The runner never accepts command text from the browser. Requests contain catalogue IDs and target IDs only.
