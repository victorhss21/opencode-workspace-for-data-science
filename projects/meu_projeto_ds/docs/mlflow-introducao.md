# Introducao ao MLflow neste projeto

Este projeto agora usa MLflow em modo remote-first, local-safe.

## Objetivo

Adicionar rastreabilidade real ao ciclo de vida do modelo, sem perder a capacidade de aprender e rodar localmente.

## Como a integracao foi pensada

- `src/meu_projeto_ds/config.py` centraliza configuracao de tracking e registry
- `src/meu_projeto_ds/models/tracking.py` concentra a integracao com MLflow
- `src/meu_projeto_ds/models/train.py` cria runs, loga metricas, artefatos e tenta registrar o modelo
- `models/registry/` continua como espelho local e pedagogico do estado mais recente

## Modo remote-first

Se estas variaveis estiverem definidas, o projeto usa o servidor configurado:

- `MLFLOW_TRACKING_URI`
- `MLFLOW_REGISTRY_URI`
- `MLFLOW_EXPERIMENT_NAME`
- `MLFLOW_MODEL_NAME`

## Modo local-safe

Se `MLFLOW_TRACKING_URI` nao estiver definida, o projeto usa fallback local em `mlruns/`.

Se o backend local nao suportar registro de modelos, o treino nao falha: ele salva o resultado, registra artifacts e informa que o registro remoto ficou indisponivel.

Esse modo local e util para estudo, testes e debug, mas nao deve ser tratado como estrategia principal para times. Para colaboracao e governanca de verdade, prefira servidor remoto com backend persistente apropriado.

## O que o treino passa a gerar

- run rastreavel no MLflow
- metricas de avaliacao
- artefato do modelo
- relatorio em `models/reports/latest-training-report.json`
- modelo serializado em `models/serialized/`
- manifesto local em `models/registry/latest-run.json`

## Como usar

### Rodar localmente

```bash
make train
make mlflow-ui
```

### Rodar apontando para servidor remoto

```bash
export MLFLOW_TRACKING_URI="https://seu-servidor-mlflow"
export MLFLOW_REGISTRY_URI="https://seu-servidor-mlflow"
export MLFLOW_EXPERIMENT_NAME="meu-projeto-ds-experiments"
export MLFLOW_MODEL_NAME="meu-projeto-ds-model"
make train
```

## O que aprender com esta fase

- a diferenca entre tracking e model registry
- como parametros, metricas e artefatos formam a memoria do treino
- por que fallback local ajuda no aprendizado e nos testes
- como preparar o projeto para promover modelos com mais seguranca
