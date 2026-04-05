# Documentacao

Espaco para guias operacionais, diagramas de fluxo, decisoes arquiteturais e materiais de estudo do projeto.

## Indice

### Fundamentos

- `docs/deep-dive-cd4ml.md`: explicacao detalhada da estrutura CD4ML criada, com foco em aprendizado e boas praticas de mercado
- `docs/adr/0001-estrutura-cd4ml.md`: decisao arquitetural que formaliza a adocao da estrutura CD4ML
- `docs/adr/0002-adocao-mlflow.md`: decisao arquitetural que formaliza a adocao de MLflow no projeto
- `docs/mlflow-introducao.md`: visao geral da integracao remote-first, local-safe com MLflow
- `docs/mlflow-tracking.md`: como o projeto registra runs, parametros, metricas e artefatos
- `docs/mlflow-model-registry.md`: como o projeto versiona modelos e prepara promocao

### Como estudar este projeto

1. Comece por `docs/deep-dive-cd4ml.md` para entender a visao geral da arquitetura.
2. Navegue pela estrutura em `data/`, `src/`, `tests/`, `pipelines/` e `models/` enquanto le o material.
3. Relacione cada pasta com o fluxo real: ingestao -> validacao -> features -> treino -> avaliacao -> registro -> inferencia -> monitoramento.
4. Depois avance para governanca de modelos e rastreabilidade, preparando o terreno para MLflow.

### Trilha de aprendizado recomendada

#### Etapa 1 - Base CD4ML

- Entender separacao entre codigo, dados, modelos, pipelines e testes
- Entender por que notebook nao deve ser a camada principal de producao
- Entender o papel de CI/CD desde o comeco do projeto

#### Etapa 2 - Reprodutibilidade

- Padronizar configuracao com `.env.example` e `src/meu_projeto_ds/config.py`
- Executar comandos recorrentes via `Makefile`
- Garantir que treino e inferencia possam ser reexecutados de forma consistente

#### Etapa 3 - Qualidade de codigo e pipeline

- Expandir testes unitarios, de integracao e de contrato
- Validar entrada de dados antes de transformar ou treinar
- Produzir relatorios de avaliacao em `models/reports/`

#### Etapa 4 - Operacionalizacao

- Evoluir `src/meu_projeto_ds/pipelines/` com fluxos reais de treino e batch inference
- Evoluir `pipelines/` com o orquestrador escolhido
- Definir criterios de promocao de modelo

#### Etapa 5 - Preparacao para MLflow

- Identificar o que precisa ser rastreado em cada execucao
- Estruturar metricas, parametros, artefatos e versoes de datasets
- Separar claramente experimento, modelo candidato e modelo promovido

### Roadmap de documentacao

- `docs/deep-dive-cd4ml.md`: documento principal ja criado
- `docs/mlflow-introducao.md`: como MLflow se encaixa nesta arquitetura
- `docs/mlflow-tracking.md`: rastreamento de experimentos, parametros, metricas e artefatos
- `docs/mlflow-model-registry.md`: versionamento, estagios e promocao de modelos
- `docs/mlflow-operacao.md`: uso de MLflow em treino, inferencia e CI/CD
- `docs/testing-ml-systems.md`: estrategia de testes para sistemas de ML
- `docs/data-contracts-and-validation.md`: validacao de dados e contratos de entrada/saida

### Perguntas-guia para estudar

- Onde uma regra descoberta em notebook deve morar quando vira padrao?
- Em que momento um dataset deixa de ser `raw` e passa a ser `processed`?
- O que precisa ser salvo para reproduzir um treino meses depois?
- Como saber qual modelo gerou uma predicao em producao?
- Como decidir quando um modelo pode ser promovido?
- Como MLflow vai ajudar sem virar apenas mais uma ferramenta no projeto?

### Ponte para MLflow

Quando avancarmos para MLflow, esta documentacao deve servir como mapa para conectar:

- `src/meu_projeto_ds/models/train.py` com tracking de parametros, metricas e artefatos
- `models/registry/` com o conceito de Model Registry
- `models/reports/` com artefatos de avaliacao logados por execucao
- `pipelines/training/` e `.github/workflows/cd-model.yml` com automacao de promocao e publicacao
- `src/meu_projeto_ds/monitoring/` com a futura observabilidade do ciclo de vida do modelo

### Convencao de crescimento da pasta `docs/`

- Cada documento novo deve ter objetivo claro e titulo orientado a aprendizado
- Prefira um documento por tema, evitando misturar fundamentos, operacao e ferramenta no mesmo arquivo
- Sempre que uma decisao arquitetural for tomada, registre tambem um ADR em `docs/adr/`
- Sempre que um novo documento for criado, atualize este indice
