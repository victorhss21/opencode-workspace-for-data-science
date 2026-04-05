from meu_projeto_ds.config import get_settings


def test_default_random_seed_is_int() -> None:
    settings = get_settings()
    assert isinstance(settings.random_seed, int)


def test_mlflow_defaults_are_defined() -> None:
    settings = get_settings()
    assert settings.mlflow_experiment_name
    assert settings.mlflow_model_name
    assert settings.mlflow_tracking_uri
