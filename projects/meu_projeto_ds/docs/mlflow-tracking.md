# MLflow Tracking

Este documento explica como o projeto usa MLflow Tracking para registrar experimentos, parametros, metricas e artefatos de treino.

## O que e tracking

Tracking e a camada do MLflow responsavel por registrar a historia de cada execucao de treino.

Em vez de ter apenas um modelo final salvo em disco, o tracking responde perguntas como:

- qual configuracao gerou este resultado?
- quais metricas esse treino obteve?
- qual artifact foi produzido?
- qual run originou uma versao do modelo?

No projeto, isso comeca em `src/meu_projeto_ds/models/train.py` e e configurado por `src/meu_projeto_ds/models/tracking.py`.

## Como esta implementado aqui

### Configuracao

O setup de tracking passa por `src/meu_projeto_ds/config.py` e pelas variaveis:

- `MLFLOW_TRACKING_URI`
- `MLFLOW_EXPERIMENT_NAME`
- `MLFLOW_ARTIFACT_LOCATION`

Se `MLFLOW_TRACKING_URI` nao estiver definida, o projeto usa fallback local em `mlruns/`.

### Inicializacao

O metodo `configure_mlflow()` em `src/meu_projeto_ds/models/tracking.py` faz quatro coisas importantes:

1. configura `tracking_uri`
2. configura `registry_uri`
3. garante que o experimento exista
4. seleciona o experimento ativo para a run

Esse e um bom padrao de mercado: o codigo de treino nao deve ficar espalhando setup de cliente e criacao de experimento em varios lugares.

### Execucao de treino

Em `src/meu_projeto_ds/models/train.py`, o fluxo atual abre uma run com:

```python
with mlflow.start_run(run_name=f"{settings.mlflow_model_name}-training") as run:
```

Dentro dela, o projeto registra:

- tags do contexto da execucao
- parametros do treino
- metricas de avaliacao
- modelo no formato do MLflow
- relatorios locais como artifacts
- modelo serializado local como artifact adicional

## O que a run registra hoje

### Tags

As tags servem para classificar a execucao e facilitar busca no UI do MLflow.

Hoje o projeto grava tags como:

- `project`
- `project_env`
- `pipeline_stage`
- `tracking_mode`

### Parametros

Parametros sao entradas da execucao que ajudam a reproduzir o treino.

Hoje o projeto registra, entre outros:

- `random_seed`
- `tracking_uri`
- `registry_uri`
- `train_rows`
- `test_rows`
- `feature_count`

Na pratica, esse conjunto deve crescer conforme o pipeline amadurece.

Exemplos futuros importantes:

- versao do dataset
- versao das features
- hiperparametros do modelo
- commit hash
- nome do pipeline

### Metricas

As metricas sao calculadas por `src/meu_projeto_ds/models/evaluate.py`.

Hoje o projeto registra:

- `mae`
- `rmse`
- `sample_count`

Essas metricas sao suficientes para demonstrar o mecanismo, mas em um sistema real devem refletir o objetivo de negocio e incluir cortes relevantes.

### Artefatos

O projeto registra artefatos em dois mundos:

- no MLflow
- localmente em diretórios de apoio

Hoje, o treino gera e loga:

- relatorio em `models/reports/latest-training-report.json`
- modelo serializado em `models/serialized/meu-projeto-ds-model.pkl`
- manifesto local em `models/registry/latest-run.json`

E tambem loga esses arquivos como artifacts da run.

## Como usar na pratica

### Rodar localmente

```bash
make train
make mlflow-ui
```

Com isso, voce consegue:

- executar o treino
- abrir a UI do MLflow
- inspecionar run, params, metrics e artifacts

### Rodar com servidor remoto

```bash
export MLFLOW_TRACKING_URI="https://seu-servidor-mlflow"
export MLFLOW_REGISTRY_URI="https://seu-servidor-mlflow"
export MLFLOW_EXPERIMENT_NAME="meu-projeto-ds-experiments"
export MLFLOW_MODEL_NAME="meu-projeto-ds-model"
make train
```

Nesse caso, a run passa a ser rastreada no backend remoto, mas o projeto ainda salva artefatos locais de apoio para debug e aprendizado.

## Leitura mental correta: o que cada coisa representa

- experimento: agrupador logico de runs
- run: uma execucao especifica de treino
- parametros: entradas da run
- metricas: saidas quantitativas da run
- artifacts: arquivos gerados pela run

Um erro comum e pensar que tracking existe apenas para ver uma tabelinha de metricas. Na pratica, ele e a memoria operacional do treinamento.

## Hacks praticos que mudam o jogo

- registre sempre `dataset_version`, mesmo que seja um valor manual no inicio
- use tags para classificar objetivo do treino, ambiente e fase do pipeline
- gere um relatorio JSON pequeno e legivel por maquina junto das metricas
- padronize nomes de experimento; sem isso o servidor vira bagunca rapido
- use tracking para comparar runs, nao apenas para arquivar uma unica execucao

## O que nunca esquecer

- run sem contexto nao e reproduzivel
- metrica sem definicao de negocio nao ajuda na promocao do modelo
- artifact sem ligacao clara com a run perde valor
- tracking local e excelente para aprender, mas nao substitui backend remoto para colaboracao real
- o tracking deve registrar a historia do treino, nao apenas o resultado final

## Como esta documentacao se conecta ao codigo

- configuracao: `src/meu_projeto_ds/config.py`
- setup do cliente: `src/meu_projeto_ds/models/tracking.py`
- abertura da run e logging: `src/meu_projeto_ds/models/train.py`
- metricas: `src/meu_projeto_ds/models/evaluate.py`
- artifacts locais: `models/reports/`, `models/serialized/`, `models/registry/`

## Proximo passo natural

Depois de entender tracking, avance para `docs/mlflow-model-registry.md`.

Ali a conversa deixa de ser apenas historico de execucao e passa a ser governanca de versoes e promocao de modelos.
