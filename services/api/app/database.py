import json
import sqlite3
from pathlib import Path

from .models import RunRecord


class RunRepository:
    def __init__(self, path: Path):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.path, check_same_thread=False)
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS runs (
                    id TEXT PRIMARY KEY,
                    created_at TEXT NOT NULL,
                    payload TEXT NOT NULL
                )
                """
            )

    def save(self, run: RunRecord) -> None:
        with self._connect() as connection:
            connection.execute(
                "INSERT OR REPLACE INTO runs(id, created_at, payload) VALUES (?, ?, ?)",
                (run.id, run.created_at.isoformat(), run.model_dump_json()),
            )

    def get(self, run_id: str) -> RunRecord | None:
        with self._connect() as connection:
            row = connection.execute("SELECT payload FROM runs WHERE id = ?", (run_id,)).fetchone()
        return RunRecord.model_validate_json(row["payload"]) if row else None

    def list(self) -> list[RunRecord]:
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT payload FROM runs ORDER BY created_at DESC LIMIT 100"
            ).fetchall()
        return [RunRecord.model_validate(json.loads(row["payload"])) for row in rows]
