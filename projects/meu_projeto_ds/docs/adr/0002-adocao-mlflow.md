# ADR 0002 - Adotar MLflow para tracking e versionamento de modelos

- Status: aceito
- Data: 2026-03-14

## Contexto

O projeto evoluiu da fase de estrutura inicial em CD4ML para uma fase em que treino, avaliacao e governanca de modelos precisam ser rastreaveis.

Antes da adocao de MLflow, o projeto tinha apenas organizacao local de artefatos em:

- `models/serialized/`
- `models/reports/`
- `models/registry/`

Essa estrutura continua util para aprendizado, debug e apoio operacional, mas nao e suficiente como mecanismo principal de rastreabilidade e governanca.

O projeto precisa responder de forma confiavel perguntas como:

- qual execucao gerou este modelo?
- com quais parametros e metricas esse treino foi produzido?
- qual versao do modelo foi registrada?
- como separar experimento, artefato e modelo promovivel?

Como o projeto tem vies build to learn, a solucao tambem precisa permitir estudo local sem bloquear evolucao para cenarios mais proximos de mercado.

## Decisao

Adotar MLflow como solucao padrao para:

- tracking de experimentos
- logging de parametros, metricas e artefatos
- registro e versionamento de modelos
- preparacao de promocao controlada de modelos

A adocao segue o principio `remote-first, local-safe`:

- em ambientes colaborativos ou operacionais, o projeto deve preferir servidor remoto de MLflow
- em ambiente local, estudo e testes, o projeto pode usar fallback seguro em `mlruns/`

O MLflow passa a ser a fonte principal de verdade para tracking e model registry.

Os diretorios locais continuam com papel complementar:

- `models/reports/` para evidencias locais de avaliacao
- `models/serialized/` para artefatos locais de apoio
- `models/registry/` para manifests locais de debug e aprendizado

## Consequencias

### Positivas

- o projeto ganha rastreabilidade real de treino
- a separacao entre run, artifact e model version fica explicita
- o caminho para promocao por estagios fica aberto
- CI/CD pode evoluir para automacao de registro e promocao
- a base fica mais alinhada com praticas de mercado em MLOps

### Custos e trade-offs

- a arquitetura ganha uma dependencia adicional e novos conceitos para aprender
- backend local por filesystem e util para estudo, mas nao deve ser tratado como estrategia principal de longo prazo
- o time precisa manter disciplina sobre nomes de experimentos, modelos, metricas e criterios de promocao

### Implicacoes de implementacao

- configuracao centralizada em `src/meu_projeto_ds/config.py`
- integracao com MLflow concentrada em `src/meu_projeto_ds/models/tracking.py`
- treino com logging e registro em `src/meu_projeto_ds/models/train.py`
- documentacao dedicada em `docs/mlflow-introducao.md`, `docs/mlflow-tracking.md` e `docs/mlflow-model-registry.md`

## O que esta fora do escopo deste ADR

Este ADR nao define ainda:

- criterios formais de promocao para `Staging` e `Production`
- estrategia definitiva de autenticacao no servidor remoto
- politica de aliases, estagios ou rollback de modelos
- integracao com monitoramento pos-deploy

Esses temas devem aparecer em ADRs e documentos posteriores conforme o projeto amadurecer.
