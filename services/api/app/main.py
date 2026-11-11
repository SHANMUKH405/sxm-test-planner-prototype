from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from .adapters.catalog import DemoCatalogueAdapter, RobotCatalogueAdapter
from .adapters.runner import LocalRobotRunnerAdapter, SimulatedRunnerAdapter
from .adapters.targets import get_targets
from .database import RunRepository
from .models import CreateRunRequest, RunRecord, Target, TestDefinition
from .services import PlannerService
from .settings import settings

app = FastAPI(title="SXM Test Planner API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.web_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

catalogue = (
    RobotCatalogueAdapter(settings.robot_repo_root)
    if settings.catalog_mode == "robot"
    else DemoCatalogueAdapter()
)
runner = (
    LocalRobotRunnerAdapter(settings.robot_repo_root, settings.artifact_root)
    if settings.runner_mode == "robot"
    else SimulatedRunnerAdapter()
)
repository = RunRepository(settings.database_path)
planner = PlannerService(catalogue, get_targets(), runner, repository)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "catalog_mode": settings.catalog_mode, "runner_mode": settings.runner_mode}


@app.get("/api/catalog", response_model=list[TestDefinition])
def list_catalogue() -> list[TestDefinition]:
    return planner.tests()


@app.get("/api/catalog/{test_id}", response_model=TestDefinition)
def get_test(test_id: str) -> TestDefinition:
    item = next((item for item in planner.tests() if item.id == test_id), None)
    if item is None:
        raise HTTPException(404, "Test not found")
    return item


@app.get("/api/targets", response_model=list[Target])
def list_targets() -> list[Target]:
    return planner.targets


@app.get("/api/runs", response_model=list[RunRecord])
def list_runs() -> list[RunRecord]:
    return repository.list()


@app.post("/api/runs", response_model=RunRecord, status_code=202)
async def create_run(request: CreateRunRequest) -> RunRecord:
    return planner.create_run(request)


@app.get("/api/runs/{run_id}", response_model=RunRecord)
def get_run(run_id: str) -> RunRecord:
    run = repository.get(run_id)
    if run is None:
        raise HTTPException(404, "Run not found")
    return run


@app.post("/api/runs/{run_id}/cancel", response_model=RunRecord)
def cancel_run(run_id: str) -> RunRecord:
    return planner.cancel(run_id)


@app.get("/api/runs/{run_id}/artifacts/{artifact_name}")
def get_artifact(run_id: str, artifact_name: str) -> FileResponse:
    allowed = {"output.xml", "log.html", "report.html", "console.log"}
    if artifact_name not in allowed:
        raise HTTPException(404, "Artifact not found")
    path = (settings.artifact_root / run_id / artifact_name).resolve()
    root = settings.artifact_root.resolve()
    if root not in path.parents or not path.exists():
        raise HTTPException(404, "Artifact not found")
    return FileResponse(path)
