from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    catalog_mode: str = "demo"
    runner_mode: str = "simulate"
    robot_repo_root: Path = Path("../../demo-robot-repo")
    database_path: Path = Path("runtime/planner.db")
    artifact_root: Path = Path("runtime/artifacts")
    web_origin: str = "http://localhost:3000"


settings = Settings()
