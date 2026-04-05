import numpy as np


def evaluate(y_true: np.ndarray, y_pred: np.ndarray) -> dict:
    residuals = np.asarray(y_true, dtype=float) - np.asarray(y_pred, dtype=float)

    return {
        "mae": round(float(np.mean(np.abs(residuals))), 6),
        "rmse": round(float(np.sqrt(np.mean(np.square(residuals)))), 6),
        "sample_count": int(residuals.shape[0]),
    }
