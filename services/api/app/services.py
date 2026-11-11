import asyncio
import subprocess
import uuid
from datetime import UTC, datetime

from fastapi import HTTPException

from .adapters.catalog import CatalogueAdapter
from .adapters.runner import RunnerAdapter
from .database import RunRepository
from .models import CreateRunRequest, RunRecord, RunStatus, Target, TestDefinition


class PlannerService:
    def __init__(
        self,
        catalogue: CatalogueAdapter,
        targets: list[Target],
        runner: RunnerAdapter,
        repository: RunRepository,
    ):
        self.catalogue = catalogue
        self.targets = targets
        self.runner = runner
        self.repository = repository
        self.tasks: dict[str, asyncio.Task] = {}

    def tests(self) -> list[TestDefinition]:
        return self.catalogue.list_tests()

    def target(self, target_id: str) -> Target:
        target = next((target for target in self.targets if target.id == target_id), None)
        if target is None:
            raise HTTPException(404, "Target not found")
        return target

    def source_revision(self) -> str:
        try:
            return subprocess.check_output(
                ["git", "rev-parse", "--short", "HEAD"], text=True, timeout=2
            ).strip()
        except (OSError, subprocess.SubprocessError):
            return "unavailable"

    def create_run(self, request: CreateRunRequest) -> RunRecord:
        catalogue = {test.id: test for test in self.tests()}
        missing = [test_id for test_id in request.test_ids if test_id not in catalogue]
        if missing:
            raise HTTPException(400, f"Unknown test IDs: {', '.join(missing)}")
        tests = [catalogue[test_id] for test_id in request.test_ids]
        target = self.target(request.target_id)
        if target.status != "available":
            raise HTTPException(409, "Selected target is not available")
        required = set().union(*(test.capabilities for test in tests))
        unavailable = sorted(required - set(target.capabilities))
        if unavailable:
            raise HTTPException(409, f"Target lacks capabilities: {', '.join(unavailable)}")
        run = RunRecord(
            id=f"RUN-{uuid.uuid4().hex[:8].upper()}",
            name=request.name,
            test_ids=request.test_ids,
            target_id=request.target_id,
            status=RunStatus.QUEUED,
            source_revision=self.source_revision(),
            created_at=datetime.now(UTC),
        )
        self.repository.save(run)
        self.tasks[run.id] = asyncio.create_task(self._execute(run, tests))
        return run

    async def _execute(self, run: RunRecord, tests: list[TestDefinition]) -> None:
        async def update(updated: RunRecord) -> None:
            self.repository.save(updated)

        try:
            await self.runner.execute(run, tests, update)
        except Exception as error:
            run.status = RunStatus.BLOCKED
            run.error = str(error)
            run.finished_at = datetime.now(UTC)
            self.repository.save(run)

    def cancel(self, run_id: str) -> RunRecord:
        run = self.repository.get(run_id)
        if run is None:
            raise HTTPException(404, "Run not found")
        task = self.tasks.get(run_id)
        if task and not task.done():
            task.cancel()
            run.status = RunStatus.CANCELLED
            run.finished_at = datetime.now(UTC)
            self.repository.save(run)
        return run
