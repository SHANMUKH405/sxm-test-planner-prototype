import asyncio
import os
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Awaitable, Callable, Protocol

from robot.api import ExecutionResult

from ..models import RunRecord, RunStatus, TestDefinition, TestResult

RunUpdate = Callable[[RunRecord], Awaitable[None]]


class RunnerAdapter(Protocol):
    async def execute(self, run: RunRecord, tests: list[TestDefinition], update: RunUpdate) -> None: ...


class SimulatedRunnerAdapter:
    async def execute(self, run: RunRecord, tests: list[TestDefinition], update: RunUpdate) -> None:
        run.status = RunStatus.PREPARING
        run.started_at = datetime.now(UTC)
        await update(run)
        await asyncio.sleep(0.7)
        run.status = RunStatus.RUNNING
        await update(run)
        results = []
        for test in tests:
            await asyncio.sleep(0.9)
            results.append(
                TestResult(
                    test_id=test.id,
                    name=test.name,
                    status=RunStatus.PASSED,
                    elapsed_seconds=0.9,
                    message="Expected learning flow completed; observed simulator state retained.",
                )
            )
            run.results = list(results)
            await update(run)
        run.status = RunStatus.COLLECTING_RESULTS
        await update(run)
        await asyncio.sleep(0.4)
        run.status = RunStatus.PASSED
        run.finished_at = datetime.now(UTC)
        await update(run)


class LocalRobotRunnerAdapter:
    def __init__(self, repo_root: Path, artifact_root: Path):
        self.repo_root = repo_root.resolve()
        self.artifact_root = artifact_root.resolve()

    async def execute(self, run: RunRecord, tests: list[TestDefinition], update: RunUpdate) -> None:
        run.status = RunStatus.PREPARING
        run.started_at = datetime.now(UTC)
        await update(run)
        output_dir = (self.artifact_root / run.id).resolve()
        output_dir.mkdir(parents=True, exist_ok=True)
        if self.artifact_root not in output_dir.parents:
            raise ValueError("Unsafe artifact path")
        suites = {test.suite_path for test in tests}
        if len(suites) != 1:
            raise ValueError("Prototype local runner supports one Robot suite per cycle")
        suite_path = (self.repo_root / next(iter(suites))).resolve()
        if self.repo_root not in suite_path.parents or not suite_path.is_file():
            raise ValueError("Catalogue path is outside the approved repository root")
        args = [
            sys.executable,
            "-m",
            "robot",
            "--pythonpath",
            str(self.repo_root / "lib"),
            "--outputdir",
            str(output_dir),
        ]
        for test in tests:
            args.extend(["--test", test.name])
        args.append(str(suite_path))
        run.status = RunStatus.RUNNING
        await update(run)
        process = await asyncio.create_subprocess_exec(
            *args,
            cwd=self.repo_root,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
            env={**os.environ, "PYTHONUTF8": "1"},
        )
        stdout, _ = await process.communicate()
        (output_dir / "console.log").write_bytes(stdout)
        run.status = RunStatus.COLLECTING_RESULTS
        await update(run)
        output_xml = output_dir / "output.xml"
        results = []
        if output_xml.exists():
            result = ExecutionResult(str(output_xml))
            by_name = {test.name: test for test in tests}
            for suite in result.suite.suites:
                for robot_test in suite.tests:
                    definition = by_name.get(robot_test.name)
                    if definition:
                        results.append(
                            TestResult(
                                test_id=definition.id,
                                name=robot_test.name,
                                status=RunStatus.PASSED if robot_test.passed else RunStatus.FAILED,
                                elapsed_seconds=robot_test.elapsed_time.total_seconds(),
                                message=robot_test.message or "",
                            )
                        )
        run.results = results
        run.artifacts = [name for name in ["output.xml", "log.html", "report.html", "console.log"] if (output_dir / name).exists()]
        run.status = RunStatus.PASSED if process.returncode == 0 else RunStatus.FAILED
        run.finished_at = datetime.now(UTC)
        await update(run)
