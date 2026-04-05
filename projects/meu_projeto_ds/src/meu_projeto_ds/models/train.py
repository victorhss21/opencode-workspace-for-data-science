from datetime import UTC, datetime

import mlflow
import mlflow.sklearn
import numpy as np
from mlflow.models import infer_signature
from sklearn.linear_model import LinearRegression

from meu_projeto_ds.models.evaluate import evaluate
from meu_projeto_ds.models.tracking import (
    configure_mlflow,
    persist_run_metadata,
    register_model_version,
    serialize_model,
    write_json_artifact,
)
from meu_projeto_ds.utils.io import ensure_directory
from meu_projeto_ds.utils.logging import get_logger


logger = get_logger(__name__)


def _build_training_dataset(random_seed: int) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    rng = np.random.default_rng(random_seed)

    train_features = np.arange(1, 9, dtype=float).reshape(-1, 1)
    train_target = (3.0 * train_features.ravel()) + 5.0 + rng.normal(0.0, 0.1, size=8)
    test_features = np.array([[9.0], [10.0], [11.0]], dtype=float)
    test_target = (3.0 * test_features.ravel()) + 5.0

    return train_features, train_target, test_features, test_target


def train() -> dict:
    settings = configure_mlflow()
    timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    report_dir = ensure_directory(settings.model_dir / "reports")
    serialized_dir = ensure_directory(settings.model_dir / "serialized")

    train_features, train_target, test_features, test_target = _build_training_dataset(
        settings.random_seed,
    )

    with mlflow.start_run(run_name=f"{settings.mlflow_model_name}-training") as run:
        mlflow.set_tags(
            {
                "project": "meu-projeto-ds",
                "project_env": settings.project_env,
                "pipeline_stage": "training",
                "tracking_mode": "remote-first-local-safe",
            }
        )
        mlflow.log_params(
            {
                "random_seed": settings.random_seed,
                "tracking_uri": settings.mlflow_tracking_uri,
                "registry_uri": settings.mlflow_registry_uri,
                "train_rows": int(train_features.shape[0]),
                "test_rows": int(test_features.shape[0]),
                "feature_count": int(train_features.shape[1]),
            }
        )

        model = LinearRegression()
        model.fit(train_features, train_target)

        predictions = model.predict(test_features)
        metrics = evaluate(test_target, predictions)
        mlflow.log_metrics(metrics)

        signature = infer_signature(train_features, model.predict(train_features))
        model_info = mlflow.sklearn.log_model(
            sk_model=model,
            name="model",
            signature=signature,
            input_example=train_features[:2],
        )

        serialized_model_path = serialize_model(
            model,
            serialized_dir / f"{settings.mlflow_model_name}.pkl",
        )

        report_payload = {
            "generated_at": timestamp,
            "metrics": metrics,
            "model_name": settings.mlflow_model_name,
            "run_id": run.info.run_id,
        }
        report_path = write_json_artifact(
            report_dir / "latest-training-report.json",
            report_payload,
        )

        mlflow.log_artifact(str(report_path), artifact_path="reports")
        mlflow.log_artifact(str(serialized_model_path), artifact_path="serialized")

        registration = register_model_version(model_info.model_uri)

        summary = {
            "artifact_uri": model_info.model_uri,
            "data_dir": str(settings.data_dir),
            "experiment_name": settings.mlflow_experiment_name,
            "metrics": metrics,
            "model_dir": str(settings.model_dir),
            "model_name": settings.mlflow_model_name,
            "model_version": registration["model_version"],
            "registration_error": registration["registration_error"],
            "registration_status": registration["registration_status"],
            "registry_uri": settings.mlflow_registry_uri,
            "report_path": str(report_path),
            "run_id": run.info.run_id,
            "serialized_model_path": str(serialized_model_path),
            "status": "training-complete",
            "tracking_uri": settings.mlflow_tracking_uri,
        }

        manifest_paths = persist_run_metadata(summary)
        mlflow.log_artifact(str(manifest_paths["latest"]), artifact_path="registry")
        logger.info("Training run completed with run_id=%s", run.info.run_id)

    return summary


if __name__ == "__main__":
    print(train())
