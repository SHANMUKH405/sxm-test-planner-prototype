import hashlib
import re
from pathlib import Path
from typing import Protocol

from robot.api import TestSuiteBuilder

from ..models import DriverConfig, TestDefinition, TestReadiness


class CatalogueAdapter(Protocol):
    def list_tests(self) -> list[TestDefinition]: ...


class DemoCatalogueAdapter:
    def list_tests(self) -> list[TestDefinition]:
        common = {
            "suite_name": "Common Flow Learning",
            "suite_path": "tests/06__demo/common_flow_learning.robot",
            "product_area": "common_flow",
            "driver": DriverConfig.DEMO,
            "capabilities": ["local_simulator", "common_flow_demo"],
            "readiness": TestReadiness.READY,
            "estimated_seconds": 4,
        }
        rows = [
            ("demo-sat", "Learning - SAT-style content - Switch and return", "DEMO_SAT_STYLE"),
            ("demo-ip", "Learning - IP-style content - Switch and return", "DEMO_IP_STYLE"),
            ("demo-xtra", "Learning - Xtra-style content - Switch and return", "DEMO_XTRA_STYLE"),
        ]
        return [
            TestDefinition(
                id=test_id,
                name=name,
                documentation="Switch away from learning content and verify it after returning.",
                **common,
                tags=["demo", "learning", "common_flow", tag],
            )
            for test_id, name, tag in rows
        ]


class RobotCatalogueAdapter:
    def __init__(self, root: Path):
        self.root = root.resolve()

    def _driver_for(self, path: Path) -> DriverConfig:
        parts = set(path.parts)
        if "01__headunit" in parts:
            return DriverConfig.HEADUNIT
        if "02__sxm_emu" in parts:
            return DriverConfig.SXM_EMU
        if "03__proxy" in parts:
            return DriverConfig.PROXY
        return DriverConfig.DEMO

    def _capabilities_for(self, driver: DriverConfig) -> list[str]:
        return {
            DriverConfig.HEADUNIT: ["headunit"],
            DriverConfig.SXM_EMU: ["headunit", "sat_emulator", "proxy"],
            DriverConfig.PROXY: ["headunit", "real_sat", "proxy"],
            DriverConfig.DEMO: ["local_simulator"],
        }[driver]

    def list_tests(self) -> list[TestDefinition]:
        if not self.root.exists():
            return []
        suite = TestSuiteBuilder().build(str(self.root / "tests"))
        discovered: list[TestDefinition] = []
        for child in suite.suites:
            self._walk(child, discovered)
        return discovered

    def _walk(self, suite, output: list[TestDefinition]) -> None:
        source = Path(suite.source).resolve() if suite.source else self.root
        if self.root not in source.parents and source != self.root:
            return
        relative = source.relative_to(self.root).as_posix() if source != self.root else ""
        driver = self._driver_for(source)
        product_area = source.stem.replace("_learning", "") if source.suffix else suite.name
        for test in suite.tests:
            tags = [str(tag) for tag in test.tags]
            case_id = next((tag for tag in tags if re.fullmatch(r"C\d+", tag)), None)
            stable = hashlib.sha256(f"{relative}\0{test.name}".encode()).hexdigest()[:16]
            output.append(
                TestDefinition(
                    id=stable,
                    name=test.name,
                    suite_name=suite.name,
                    suite_path=relative,
                    product_area=product_area,
                    driver=driver,
                    tags=tags,
                    case_id=case_id,
                    documentation=test.doc or "",
                    capabilities=self._capabilities_for(driver),
                    readiness=TestReadiness.READY,
                    estimated_seconds=30,
                )
            )
        for child in suite.suites:
            self._walk(child, output)
