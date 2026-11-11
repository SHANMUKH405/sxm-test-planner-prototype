from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field


class DriverConfig(StrEnum):
    HEADUNIT = "headunit"
    SXM_EMU = "sxm_emu"
    PROXY = "proxy"
    DEMO = "demo"


class TestReadiness(StrEnum):
    READY = "ready"
    BLOCKED = "blocked"
    DISABLED = "disabled"


class RunStatus(StrEnum):
    QUEUED = "queued"
    PREPARING = "preparing"
    RUNNING = "running"
    COLLECTING_RESULTS = "collecting_results"
    PASSED = "passed"
    FAILED = "failed"
    BLOCKED = "blocked"
    CANCELLED = "cancelled"


class TestDefinition(BaseModel):
    id: str
    name: str
    suite_name: str
    suite_path: str
    product_area: str
    driver: DriverConfig
    tags: list[str] = Field(default_factory=list)
    case_id: str | None = None
    documentation: str = ""
    capabilities: list[str] = Field(default_factory=list)
    readiness: TestReadiness = TestReadiness.READY
    estimated_seconds: int = 10


class Target(BaseModel):
    id: str
    name: str
    status: str
    target_type: str
    driver: DriverConfig
    capabilities: list[str]
    description: str


class CreateRunRequest(BaseModel):
    name: str = Field(min_length=3, max_length=120)
    test_ids: list[str] = Field(min_length=1)
    target_id: str


class TestResult(BaseModel):
    test_id: str
    name: str
    status: RunStatus
    elapsed_seconds: float
    message: str = ""


class RunRecord(BaseModel):
    id: str
    name: str
    test_ids: list[str]
    target_id: str
    status: RunStatus
    source_revision: str
    created_at: datetime
    started_at: datetime | None = None
    finished_at: datetime | None = None
    results: list[TestResult] = Field(default_factory=list)
    artifacts: list[str] = Field(default_factory=list)
    error: str | None = None
