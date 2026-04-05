import pickle

import numpy as np

from meu_projeto_ds.config import get_settings


def predict(values: list[list[float]] | None = None) -> dict:
    settings = get_settings()
    model_path = settings.model_dir / "serialized" / f"{settings.mlflow_model_name}.pkl"

    if not model_path.exists():
        return {
            "model_dir": str(settings.model_dir),
            "status": "model-not-available",
        }

    with model_path.open("rb") as model_file:
        model = pickle.load(model_file)

    features = np.asarray(values or [[12.0], [13.0]], dtype=float)
    predictions = model.predict(features).tolist()

    return {
        "model_dir": str(settings.model_dir),
        "model_path": str(model_path),
        "predictions": predictions,
        "status": "prediction-complete",
    }


if __name__ == "__main__":
    print(predict())
