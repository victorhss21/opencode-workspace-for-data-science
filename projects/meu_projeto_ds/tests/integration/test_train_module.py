from pathlib import Path

from meu_projeto_ds.models.train import train


def test_train_returns_mlflow_metadata(tmp_path, monkeypatch) -> None:
    tracking_dir = (tmp_path / "mlruns").resolve()
    monkeypatch.setenv("MODEL_DIR", str(tmp_path / "models"))
    monkeypatch.setenv("MLFLOW_TRACKING_URI", tracking_dir.as_uri())
    monkeypatch.setenv("MLFLOW_REGISTRY_URI", tracking_dir.as_uri())
    monkeypatch.setenv("MLFLOW_EXPERIMENT_NAME", "integration-test-experiment")
    monkeypatch.setenv("MLFLOW_MODEL_NAME", "integration-test-model")

    result = train()

    assert result["status"] == "training-complete"
    assert result["run_id"]
    assert result["experiment_name"] == "integration-test-experiment"
    assert result["model_name"] == "integration-test-model"
    assert Path(result["report_path"]).exists()
    assert Path(result["serialized_model_path"]).exists()
    assert result["registration_status"] in {"registered", "unavailable"}
