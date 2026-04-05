# Meu Projeto DS

Estrutura inicial seguindo principios de CD4ML para projetos de ciencia de dados e machine learning.

## Objetivos da estrutura

- separar dados, codigo, modelos e documentacao
- facilitar reproducibilidade, testes e automacao
- preparar o projeto para CI/CD e evolucao de pipelines

## Estrutura principal

```text
.
|- .github/workflows/      # automacao de CI/CD
|- data/                   # dados por estagio de maturidade
|- docs/                   # documentacao e decisoes arquiteturais
|- models/                 # artefatos de modelos e relatorios
|- notebooks/              # exploracao e experimentacao
|- pipelines/              # definicoes de pipelines operacionais
|- src/meu_projeto_ds/     # codigo-fonte versionado
|- tests/                  # testes unitarios, integracao e contrato
|- Makefile                # atalhos de desenvolvimento
|- .env.example            # variaveis de ambiente de exemplo
```

## Fluxo sugerido

1. Ingerir dados em `data/raw/` e `data/external/`.
2. Validar e transformar para `data/interim/`, `data/processed/` e `data/features/`.
3. Treinar e avaliar modelos com codigo em `src/meu_projeto_ds/`.
4. Salvar artefatos em `models/serialized/` e registros em `models/registry/`.
5. Automatizar verificacoes em CI e publicacao de artefatos em CD.

## Comandos uteis

```bash
make install
make format
make lint
make test
make train
make mlflow-ui
```

## MLflow

O projeto esta preparado para operar em modo remote-first, local-safe.

- se `MLFLOW_TRACKING_URI` e `MLFLOW_REGISTRY_URI` estiverem configurados, o treino tenta usar o servidor remoto
- se essas variaveis nao estiverem definidas, o projeto faz fallback para um backend local seguro em `mlruns/`
- os artefatos locais continuam sendo refletidos em `models/reports/`, `models/serialized/` e `models/registry/`
- para uso colaborativo e governanca real, prefira backend remoto com banco ou servico dedicado; o fallback local existe para aprendizado e testes
