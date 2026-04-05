import os
from dataclasses import dataclass
from pathlib import Path


def _env_value(name: str, default: str) -> str:
    value = os.getenv(name)
    if value is None:
        return default

    stripped_value = value.strip()
    return stripped_value or default


def _env_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default

    return value.strip().lower() in {"1", "true", "yes", "on"}


def _resolve_path(value: str, project_root: Path) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path

    return project_root / path


def _resolve_local_uri(directory_name: str, project_root: Path) -> str:
    return (project_root / directory_name).resolve().as_uri()


@dataclass(frozen=True)
class Settings:
    project_root: Path
    project_env: str
    data_dir: Path
    model_dir: Path
    log_level: str
    random_seed: int
    mlflow_tracking_uri: str
    mlflow_registry_uri: str
    mlflow_experiment_name: str
    mlflow_model_name: str
    mlflow_artifact_location: str | None
    mlflow_enable_registry: bool


def get_settings() -> Settings:
    project_root = Path(__file__).resolve().parents[2]
    tracking_uri = _env_value(
        "MLFLOW_TRACKING_URI",
        _resolve_local_uri("mlruns", project_root),
    )
    registry_uri = _env_value("MLFLOW_REGISTRY_URI", tracking_uri)
    artifact_location = os.getenv("MLFLOW_ARTIFACT_LOCATION")

    return Settings(
        project_root=project_root,
        project_env=_env_value("PROJECT_ENV", "dev"),
        data_dir=_resolve_path(_env_value("DATA_DIR", "data"), project_root),
        model_dir=_resolve_path(_env_value("MODEL_DIR", "models"), project_root),
        log_level=_env_value("LOG_LEVEL", "INFO"),
        random_seed=int(_env_value("RANDOM_SEED", "42")),
        mlflow_tracking_uri=tracking_uri,
        mlflow_registry_uri=registry_uri,
        mlflow_experiment_name=_env_value(
            "MLFLOW_EXPERIMENT_NAME",
            "meu-projeto-ds-experiments",
        ),
        mlflow_model_name=_env_value(
            "MLFLOW_MODEL_NAME",
            "meu-projeto-ds-model",
        ),
        mlflow_artifact_location=artifact_location.strip()
        if artifact_location and artifact_location.strip()
        else None,
        mlflow_enable_registry=_env_bool("MLFLOW_ENABLE_REGISTRY", True),
    )


settings = get_settings()
