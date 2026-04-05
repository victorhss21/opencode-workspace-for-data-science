PYTHON ?= python
PACKAGE = meu_projeto_ds

.PHONY: install format lint test train predict mlflow-ui

install:
	uv sync

format:
	uv run black src tests
	uv run isort src tests

lint:
	uv run flake8 src tests

test:
	uv run pytest

train:
	uv run python -m $(PACKAGE).models.train

predict:
	uv run python -m $(PACKAGE).models.predict

mlflow-ui:
	uv run mlflow ui --backend-store-uri $${MLFLOW_TRACKING_URI:-$$(pwd)/mlruns}
