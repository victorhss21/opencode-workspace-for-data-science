import json
import pickle
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import mlflow
from mlflow import MlflowClient
from mlflow.exceptions import MlflowException

from meu_projeto_ds.config import Settings, get_settings
from meu_projeto_ds.utils.io import ensure_directory


def configure_mlflow() -> Settings:
    settings = get_settings()

    mlflow.set_tracking_uri(settings.mlflow_tracking_uri)
    mlflow.set_registry_uri(settings.mlflow_registry_uri)

    client = MlflowClient()
    experiment = client.get_experiment_by_name(settings.mlflow_experiment_name)
    if experiment is None:
        create_kwargs: dict[str, str] = {}
        if settings.mlflow_artifact_location:
            create_kwargs["artifact_location"] = settings.mlflow_artifact_location
        try:
            client.create_experiment(
                settings.mlflow_experiment_name,
                **create_kwargs,
            )
        except MlflowException:
            pass

    mlflow.set_experiment(settings.mlflow_experiment_name)
    return settings


def serialize_model(model: Any, destination: Path) -> Path:
    ensure_directory(destination.parent)
    with destination.open("wb") as serialized_model:
        pickle.dump(model, serialized_model)
    return destination


def write_json_artifact(destination: Path, payload: dict[str, Any]) -> Path:
    ensure_directory(destination.parent)
    destination.write_text(json.dumps(payload, indent=2), encoding="ascii")
    return destination


def register_model_version(model_uri: str) -> dict[str, Any]:
    settings = get_settings()
    if not settings.mlflow_enable_registry:
        return {
            "registration_status": "disabled",
            "registered_model_name": settings.mlflow_model_name,
            "model_version": None,
            "registration_error": None,
        }

    client = MlflowClient()

    try:
        client.create_registered_model(settings.mlflow_model_name)
    except MlflowException as exc:
        if "already exists" not in str(exc).lower():
            return {
                "registration_status": "unavailable",
                "registered_model_name": settings.mlflow_model_name,
                "model_version": None,
                "registration_error": str(exc),
            }

    try:
        model_version = mlflow.register_model(
            model_uri=model_uri,
            name=settings.mlflow_model_name,
        )
        return {
            "registration_status": "registered",
            "registered_model_name": settings.mlflow_model_name,
            "model_version": model_version.version,
            "registration_error": None,
        }
    except Exception as exc:
        return {
            "registration_status": "unavailable",
            "registered_model_name": settings.mlflow_model_name,
            "model_version": None,
            "registration_error": str(exc),
        }


def persist_run_metadata(summary: dict[str, Any]) -> dict[str, Path]:
    settings = get_settings()
    registry_dir = ensure_directory(settings.model_dir / "registry")
    timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    latest_path = registry_dir / "latest-run.json"
    history_path = registry_dir / f"{settings.mlflow_model_name}-{timestamp}.json"

    write_json_artifact(latest_path, summary)
    write_json_artifact(history_path, summary)

    return {"latest": latest_path, "history": history_path}
