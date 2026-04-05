# Deep Dive da Estrutura CD4ML

Voce agora tem uma espinha dorsal de CD4ML pensada para aprender do jeito certo: estrutura simples o bastante para navegar, mas ja alinhada com praticas reais de times de dados que precisam sair de notebook solto para algo reproduzivel, testavel e implantavel.

Este documento faz um deep dive por elemento da estrutura criada em `/workspace`, cobrindo sempre:

- O que é?
- Para que serve?
- Como usar na pratica?
- Quando costuma ser populado no pipeline?
- Hacks praticos!
- O que nunca esquecer!

## Visao Geral

A estrutura criada foi esta, em essencia:

```text
/workspace
|- .github/workflows/
|  |- ci.yml
|  \- cd-model.yml
|- data/
|  |- raw/
|  |- external/
|  |- interim/
|  |- processed/
|  \- features/
|- docs/
|  |- README.md
|  \- adr/
|     \- 0001-estrutura-cd4ml.md
|- models/
|  |- registry/
|  |- serialized/
|  \- reports/
|- notebooks/
|  |- exploration/
|  |- experiments/
|  |- production/
|  \- README.md
|- pipelines/
|  |- training/
|  |- scoring/
|  |- monitoring/
|  \- README.md
|- src/meu_projeto_ds/
|  |- __init__.py
|  |- config.py
|  |- data/
|  |- features/
|  |- models/
|  |- pipelines/
|  |- monitoring/
|  \- utils/
|- tests/
|  |- conftest.py
|  |- unit/
|  |- integration/
|  \- contract/
|- .env.example
|- .gitignore
|- Makefile
\- README.md
```

O padrao mental mais importante aqui e:

- `data/` guarda artefatos de dados
- `src/` guarda logica versionada
- `notebooks/` guarda exploracao e experimentacao humana
- `pipelines/` guarda desenho operacional
- `models/` guarda artefatos e evidencias de modelo
- `tests/` garante confianca
- `.github/workflows/` automatiza qualidade e entrega
- `docs/` registra decisoes e contexto

Isso e CD4ML na pratica: fluxo continuo de dados, codigo, validacao, treino, empacotamento e entrega.

## Raiz do Projeto

### `README.md`

- O que e: o ponto de entrada humano do projeto.
- Para que serve: explicar intencao, estrutura, fluxo e comandos principais.
- Como usar na pratica: sempre atualize quando o projeto mudar de fase; trate como o mapa que ajuda qualquer pessoa a comecar em 5 minutos.
- Quando e populado: no inicio do projeto e depois continuamente, conforme a operacao amadurece.
- Hacks praticos:
  - mantenha um bloco "como rodar localmente"
  - inclua "fonte da verdade" para dados, treino e deploy
  - adicione um diagrama simples do fluxo
- O que nunca esquecer:
  - README desatualizado e pior que README curto
  - ele deve responder rapido: o que e, como rodar, onde mexer, como testar

### `.gitignore`

- O que e: regras do Git para nao versionar lixo, segredos e artefatos grandes.
- Para que serve: evitar versionar cache, ambiente virtual, dados brutos, modelos serializados e arquivos locais.
- Como usar na pratica: ajuste sempre que surgir novo artefato local, novo framework ou nova ferramenta.
- Quando e populado: logo no inicio; vai evoluindo junto com o projeto.
- Hacks praticos:
  - ignore diretorios de dados e modelos, mas mantenha `.gitkeep`
  - revise depois de rodar notebooks, testes e pipelines
  - trate esse arquivo como barreira anti-caos
- O que nunca esquecer:
  - `.gitignore` nao protege segredos ja commitados
  - dados pesados e modelos binarios quase nunca devem ir para o Git puro

### `.env.example`

- O que e: template de variaveis de ambiente.
- Para que serve: padronizar configuracao local, CI e producao sem commitar segredos.
- Como usar na pratica: copie para `.env` localmente; em CI/prod, injete valores via secrets/variaveis do provedor.
- Quando e populado: no setup inicial e sempre que uma nova configuracao for introduzida.
- Hacks praticos:
  - inclua comentarios curtos no futuro quando as variaveis crescerem
  - mantenha nomes claros: `MODEL_DIR`, `DATA_DIR`, `RANDOM_SEED`
  - agrupe por dominio: dados, treino, inferencia, observabilidade
- O que nunca esquecer:
  - `.env.example` mostra nomes e formatos, nunca segredos reais
  - variavel sem dono vira divida tecnica silenciosa

### `Makefile`

- O que e: atalhos operacionais para tarefas repetitivas.
- Para que serve: reduzir tribal knowledge e padronizar comandos como instalar, formatar, testar, treinar.
- Como usar na pratica: rode `make install`, `make test`, `make train`; em times, isso evita cada um inventar um comando diferente.
- Quando e populado: desde o inicio, conforme workflows vao ficando repetitivos.
- Hacks praticos:
  - trate o `Makefile` como interface do projeto
  - adicione metas como `make smoke`, `make clean`, `make notebook`, `make ci-local`
  - use para encadear qualidade: format + lint + tests
- O que nunca esquecer:
  - se o `README.md` disser uma coisa e o `Makefile` fizer outra, o time sofre
  - nao esconda logica critica demais nele; workflows complexos merecem script dedicado

## Automacao e Entrega

### `.github/workflows/ci.yml`

- O que e: pipeline de integracao continua no GitHub Actions.
- Para que serve: validar qualidade do projeto a cada push/PR.
- Como usar na pratica: ao abrir PR, o workflow roda setup de Python, instala dependencias e executa checks.
- Quando e populado: desde cedo, antes mesmo do primeiro modelo de verdade.
- Hacks praticos:
  - em DS, CI nao precisa treinar modelo pesado; foque em testes rapidos, lint e smoke tests
  - use dados sinteticos pequenos para testes
  - no futuro, adicione cache de dependencias e matriz de versoes
- O que nunca esquecer:
  - CI deve ser rapido; pipeline lento demais vira algo que o time ignora
  - so suba checks que voce esta disposto a manter verdes

### `.github/workflows/cd-model.yml`

- O que e: workflow de entrega continua para empacotamento/liberacao orientada a modelo.
- Para que serve: preparar release quando houver tag ou execucao manual.
- Como usar na pratica: em um fluxo maduro, isso valida, empacota e publica artefatos de modelo ou pacote Python.
- Quando e populado: depois que o projeto ja tem CI minima e algum caminho de release.
- Hacks praticos:
  - comece simples: testar, buildar, subir artifact
  - quando entrar MLflow, esse workflow pode registrar modelo e anexar metadados
  - use `workflow_dispatch` para experimentos controlados
- O que nunca esquecer:
  - CD de modelo nao e so salvar arquivo; precisa de rastreabilidade, versao, metricas e criterio de promocao
  - nunca publique modelo sem evidencia de qualidade

## Documentacao e Decisao Arquitetural

### `docs/README.md`

- O que e: porta de entrada da documentacao interna.
- Para que serve: orientar onde estao guias, decisoes, runbooks, diagramas e processos.
- Como usar na pratica: centralize aqui links para onboarding, dados, pipelines, observabilidade e deploy.
- Quando e populado: cedo, e vai amadurecendo conforme o projeto deixa de ser pessoal e vira colaborativo.
- Hacks praticos:
  - adicione documentos vivos: checklist de release, definicao de pronto, runbook de falhas
  - mantenha indice simples e navegavel
- O que nunca esquecer:
  - documentacao boa reduz dependencia de uma unica pessoa

### `docs/adr/0001-estrutura-cd4ml.md`

- O que e: ADR, Architecture Decision Record.
- Para que serve: registrar por que a estrutura CD4ML foi escolhida.
- Como usar na pratica: crie novos ADRs para decisoes relevantes, como adotar MLflow, usar feature store, usar batch em vez de online.
- Quando e populado: no momento da decisao arquitetural.
- Hacks praticos:
  - escreva ADR curto: contexto, decisao, consequencias
  - nao use ADR para documentar tudo; use para decisoes que seria caro rediscutir do zero
- O que nunca esquecer:
  - ADR nao e burocracia; e memoria institucional
  - registre o porque, nao so o que

## Dados

A pasta `data/` representa o ciclo de maturidade do dado. Essa e uma das partes mais importantes do CD4ML porque forca disciplina no fluxo.

### `data/raw/`

- O que e: dados brutos, recebidos da fonte, sem transformacao.
- Para que serve: preservar a entrada original do pipeline.
- Como usar na pratica: grave copias imutaveis ou snapshots; se vier CSV de fornecedor, ele entra aqui.
- Quando e populado: logo na ingestao.
- Hacks praticos:
  - trate como somente leitura
  - se possivel, nomeie com data/hora/particao
  - guarde checksums ou manifestos
- O que nunca esquecer:
  - nao limpe manualmente dado em `raw/`
  - se voce altera `raw/`, perde reprodutibilidade

### `data/external/`

- O que e: dados obtidos de fontes externas ao pipeline principal.
- Para que serve: separar claramente dependencias de terceiros, enriquecimentos e datasets de referencia.
- Como usar na pratica: tabelas de calendario, dados demograficos, benchmarks publicos, lookup tables.
- Quando e populado: na ingestao complementar ou sincronizacao externa.
- Hacks praticos:
  - documente origem, licenca e atualizacao esperada
  - guarde versao/fonte no nome ou metadata
- O que nunca esquecer:
  - dado externo muda; quando muda, seu modelo pode mudar junto sem voce perceber

### `data/interim/`

- O que e: dados intermediarios apos limpeza ou transformacao parcial.
- Para que serve: quebrar pipelines longos em etapas auditaveis.
- Como usar na pratica: depois de validar schema, remover registros invalidos, padronizar tipos, juntar fontes.
- Quando e populado: apos ingestao e validacao inicial.
- Hacks praticos:
  - salve outputs intermediarios quando a etapa anterior for cara
  - otimo lugar para debug de pipeline
- O que nunca esquecer:
  - `interim` e transitorio, mas nao baguncado; precisa de convencao clara

### `data/processed/`

- O que e: dado pronto para treino, avaliacao ou scoring.
- Para que serve: separar dataset curado do bruto e do intermediario.
- Como usar na pratica: dataset final com colunas selecionadas, tratamento aplicado e formato padronizado.
- Quando e populado: depois de transformacao de negocio e preparacao para modelagem.
- Hacks praticos:
  - gere datasets por objetivo: treino, validacao, teste, inferencia
  - associe versao do codigo que gerou esse dado
- O que nunca esquecer:
  - `processed` sem definicao formal vira pasta-coringa e bagunca o projeto

### `data/features/`

- O que e: features derivadas, prontas para alimentar modelos.
- Para que serve: isolar engenharia de atributos da mera limpeza de dados.
- Como usar na pratica: agregacoes, encodings, estatisticas temporais, janelas, embeddings tabulares, etc.
- Quando e populado: apos feature engineering.
- Hacks praticos:
  - separe feature generation de model training
  - nomeie outputs por versao de conjunto de features
  - no futuro, essa pasta conversa muito bem com feature store ou MLflow artifacts
- O que nunca esquecer:
  - features vazam informacao com facilidade; pense sempre em leakage temporal e leakage de target

### `.gitkeep` em `data/*`

- O que e: arquivo vazio para manter pasta no Git.
- Para que serve: versionar a estrutura sem versionar o conteudo dos dados.
- Como usar na pratica: deixe apenas como placeholder.
- Quando e populado: na criacao da estrutura.
- Hacks praticos:
  - pode trocar por `README.md` local explicando o proposito da pasta
- O que nunca esquecer:
  - a presenca da pasta nao significa que deva haver dados no Git

## Modelos

### `models/registry/`

- O que e: espaco conceitual para versoes, promovidos e metadata de modelos.
- Para que serve: organizar o estado do ciclo de vida do modelo.
- Como usar na pratica: hoje pode ter manifests, metadados e links; depois pode refletir registros do MLflow.
- Quando e populado: quando um modelo deixa de ser so experimento e comeca a ser candidato/release.
- Hacks praticos:
  - comece guardando `model_name`, `version`, `metrics`, `dataset_version`, `code_version`
  - depois conecte isso a MLflow Model Registry
- O que nunca esquecer:
  - registry nao e so armazenamento; e governanca

### `models/serialized/`

- O que e: artefatos serializados de modelo, como `.pkl`, `.joblib`, `.onnx`.
- Para que serve: guardar o binario do modelo treinado.
- Como usar na pratica: pipeline de treino escreve aqui localmente; CI/CD pode anexar artifacts.
- Quando e populado: apos treino/aprovacao de modelo.
- Hacks praticos:
  - nunca trate esse diretorio como deposito eterno
  - use convencao clara: modelo, versao, data, hash
  - mantenha metadata ao lado do binario
- O que nunca esquecer:
  - modelo binario sem contexto nao serve
  - serializacao depende de versao de biblioteca; ambiente importa

### `models/reports/`

- O que e: relatorios de avaliacao e evidencias do desempenho do modelo.
- Para que serve: guardar metricas, graficos, matrizes de confusao, feature importance, fairness checks.
- Como usar na pratica: cada treino relevante deve gerar evidencias auditaveis aqui.
- Quando e populado: apos avaliacao do modelo.
- Hacks praticos:
  - salve tanto HTML/Markdown quanto JSON de metricas
  - isso ajuda muito em PR review e governanca
- O que nunca esquecer:
  - sem relatorio, a promocao do modelo vira opiniao

### `.gitkeep` em `models/*`

- O que e: placeholder para versionar estrutura.
- Para que serve: manter pastas vazias no Git.
- Como usar na pratica: nao mexa.
- Quando e populado: na criacao da base.
- O que nunca esquecer:
  - nao confundir estrutura com estrategia de versionamento real; MLflow/DVC resolvem isso melhor

## Notebooks

### `notebooks/README.md`

- O que e: explicacao da estrategia para notebooks.
- Para que serve: impedir que notebook vire terra sem lei.
- Como usar na pratica: deixe claro o proposito de cada subpasta e o que deve ou nao entrar ali.
- Quando e populado: logo no inicio.
- Hacks praticos:
  - adicione convencao de nome, por exemplo `2026-03-13_eda-target-drift.ipynb`
- O que nunca esquecer:
  - notebook sem regra vira codigo invisivel, impossivel de revisar

### `notebooks/exploration/`

- O que e: area de analise exploratoria.
- Para que serve: entender dados, distribuicoes, qualidade, anomalias, hipoteses.
- Como usar na pratica: EDA, profiling, graficos, inspecao manual.
- Quando e populado: inicio do ciclo, logo apos ingestao.
- Hacks praticos:
  - transforme descobertas importantes em codigo de `src/` o mais cedo possivel
  - se o notebook revelou regra de limpeza, essa regra nao deve morar so no notebook
- O que nunca esquecer:
  - EDA e para descobrir, nao para operacionalizar

### `notebooks/experiments/`

- O que e: area de experimentacao de modelagem.
- Para que serve: testar hipoteses, features, algoritmos e comparacoes.
- Como usar na pratica: benchmark entre modelos, tuning inicial, analises de erro.
- Quando e populado: fase de experimentacao e selecao de abordagem.
- Hacks praticos:
  - registre sempre dataset usado, seed e metrica
  - quando o experimento vencer, promova a logica para `src/meu_projeto_ds/`
- O que nunca esquecer:
  - experimento bom que nao e promovido a codigo versionado nao escala

### `notebooks/production/`

- O que e: notebooks de referencia mais proximos do fluxo produtivo.
- Para que serve: explicar pipelines, demonstrar uso, apoiar handoff ou troubleshooting.
- Como usar na pratica: um notebook reproduzivel que mostra como carregar features, aplicar modelo e validar saida.
- Quando e populado: depois que ja existe fluxo estavel.
- Hacks praticos:
  - use como documento executavel para onboarding
  - otimo para mostrar happy path do pipeline
- O que nunca esquecer:
  - production notebook nao substitui pipeline real; ele complementa

### `.gitkeep` em notebooks

- O que e: placeholder estrutural.
- O que nunca esquecer:
  - crie poucos notebooks bem nomeados; muitos notebooks soltos poluem rapido

## Pipelines

A pasta `pipelines/` representa o lado operacional do CD4ML, nao necessariamente a implementacao Python em si.

### `pipelines/README.md`

- O que e: guia de organizacao dos pipelines.
- Para que serve: separar treino, scoring e monitoramento conceitualmente.
- Como usar na pratica: aqui entram YAMLs, DAGs, manifests, jobs, templates do orquestrador escolhido.
- Quando e populado: quando a operacao deixa de ser manual.
- Hacks praticos:
  - mantenha o desenho operacional aqui, mesmo que parte da logica esteja em `src/`
- O que nunca esquecer:
  - pipeline operacional nao deve virar copia da logica de negocio; ele deve orquestrar, nao reimplementar tudo

### `pipelines/training/`

- O que e: espaco para definicao operacional do treino.
- Para que serve: organizar jobs de extracao, preparacao, treino, avaliacao e publicacao.
- Como usar na pratica: no futuro pode conter DAG Airflow, pipeline Kubeflow, workflow GitHub Actions, script runner.
- Quando e populado: quando treino vira recorrente.
- Hacks praticos:
  - separe passos explicitamente: ingest, validate, feature, train, evaluate, register
  - esse particionamento ajuda muito observabilidade e retry
- O que nunca esquecer:
  - treino recorrente sem validacao de input e receita para desastre silencioso

### `pipelines/scoring/`

- O que e: espaco para inferencia em lote ou geracao de predicoes.
- Para que serve: operacionalizar scoring sobre novos dados.
- Como usar na pratica: jobs batch diarios, semanais, event-driven, geracao de tabela de saida.
- Quando e populado: quando o modelo ja esta pronto para servir valor.
- Hacks praticos:
  - faca scoring idempotente
  - grave input, output, versao de modelo e timestamp
- O que nunca esquecer:
  - sem rastrear qual versao do modelo gerou qual saida, voce perde auditabilidade

### `pipelines/monitoring/`

- O que e: espaco para jobs de monitoramento.
- Para que serve: detectar drift, quebra de schema, queda de qualidade, volume anomalo, latencia, cobertura.
- Como usar na pratica: scripts/jobs de monitoramento periodico, alertas, dashboards.
- Quando e populado: idealmente junto do primeiro deploy relevante, nao meses depois.
- Hacks praticos:
  - monitoramento comeca com checks simples: linha, nulos, cardinalidade, distribuicao
  - nao espere MLflow ou plataforma sofisticada para comecar
- O que nunca esquecer:
  - modelo sem monitoramento ja esta degradando; voce so ainda nao viu

### `README.md` em cada subpasta de `pipelines/`

- O que e: documentacao local da finalidade da subpasta.
- Para que serve: reduzir ambiguidade para futuros arquivos operacionais.
- Como usar na pratica: evolua esses READMEs para explicar gatilhos, entradas, saidas e dependencias.
- Quando e populado: logo no setup e refinado com o tempo.
- O que nunca esquecer:
  - documente contrato operacional: o que entra, o que sai, com que frequencia, com qual SLA

## Codigo-fonte

A pasta `src/meu_projeto_ds/` e o coracao do software de ML. CD4ML maduro promove logica para codigo versionado testavel.

### `src/meu_projeto_ds/__init__.py`

- O que e: marcador de pacote Python e local de versao basica.
- Para que serve: permitir imports organizados e expor `__version__`.
- Como usar na pratica: pacote central do projeto.
- Quando e populado: no setup inicial.
- Hacks praticos:
  - mais tarde, centralize versao com ferramenta de release se quiser
- O que nunca esquecer:
  - pacote bem definido evita imports frageis espalhados

### `src/meu_projeto_ds/config.py`

- O que e: configuracao centralizada via variaveis de ambiente.
- Para que serve: evitar strings hardcoded e espalhamento de configuracao.
- Como usar na pratica: qualquer modulo acessa `settings` para paths e parametros basicos.
- Quando e populado: desde o inicio; cresce conforme o projeto amadurece.
- Hacks praticos:
  - centralizar config e uma das maiores alavancas de organizacao
  - depois vale evoluir para `pydantic-settings` ou validacao mais forte
- O que nunca esquecer:
  - config sem validacao gera bugs silenciosos
  - paths relativos precisam ser tratados com cuidado em CI e producao

### Pacote `src/meu_projeto_ds/data/`

#### `src/meu_projeto_ds/data/__init__.py`

- O que e: namespace da camada de dados.
- Para que serve: organizar ingestao e validacao.
- O que nunca esquecer:
  - dados sao dominio proprio; nao jogue tudo em `utils/`

#### `src/meu_projeto_ds/data/ingestion.py`

- O que e: modulo de ingestao.
- Para que serve: encapsular logica de acesso, caminhos e fontes.
- Como usar na pratica: funcoes para baixar, ler, persistir ou localizar dados brutos.
- Quando e populado: logo no comeco da construcao do pipeline.
- Hacks praticos:
  - faca funcoes pequenas e previsiveis
  - padronize entradas e saidas com `Path` e DataFrames
- O que nunca esquecer:
  - ingestao deve ser reexecutavel e idempotente

#### `src/meu_projeto_ds/data/validation.py`

- O que e: modulo de validacao de entrada.
- Para que serve: garantir que o dado existe e respeita contratos minimos.
- Como usar na pratica: checks de schema, tipos, ranges, chaves, duplicidade, datas.
- Quando e populado: entre ingestao e transformacao.
- Hacks praticos:
  - pequenos validadores economizam horas de debug
  - no futuro, pode evoluir para Great Expectations, Pandera ou regras proprias
- O que nunca esquecer:
  - validacao nao e luxo; e protecao do pipeline

### Pacote `src/meu_projeto_ds/features/`

#### `src/meu_projeto_ds/features/__init__.py`

- O que e: namespace de feature engineering.
- Para que serve: separar engenharia de atributos da camada de dados e da de modelos.

#### `src/meu_projeto_ds/features/engineering.py`

- O que e: modulo de construcao de features.
- Para que serve: transformar dado processado em entradas uteis ao modelo.
- Como usar na pratica: funcoes puras que recebem dados e devolvem conjunto de features.
- Quando e populado: apos entendimento do dado e definicao da estrategia de modelagem.
- Hacks praticos:
  - mantenha engenharia de atributos deterministica
  - separe fit/transform quando fizer sentido
  - documente features derivadas mais sensiveis
- O que nunca esquecer:
  - feature leakage e um dos erros mais comuns e caros em ML aplicado

### Pacote `src/meu_projeto_ds/models/`

#### `src/meu_projeto_ds/models/__init__.py`

- O que e: namespace da camada de modelagem.

#### `src/meu_projeto_ds/models/train.py`

- O que e: ponto de entrada de treino.
- Para que serve: centralizar a execucao do ciclo de treinamento.
- Como usar na pratica: recebe dataset, features e config, treina, avalia e salva artefatos.
- Quando e populado: quando o primeiro baseline sai do notebook.
- Hacks praticos:
  - faca o treino retornar metadata util
  - sempre logue seed, dataset, parametros e metricas
- O que nunca esquecer:
  - treino sem rastreabilidade nao e reproduzivel

#### `src/meu_projeto_ds/models/predict.py`

- O que e: ponto de entrada de inferencia.
- Para que serve: aplicar modelo salvo a novos dados.
- Como usar na pratica: carregar artefato, validar entrada, transformar e prever.
- Quando e populado: quando o modelo comeca a gerar valor fora do treino.
- Hacks praticos:
  - trate inferencia como produto: entrada bem definida, saida consistente
  - se scoring batch, salve metadata junto
- O que nunca esquecer:
  - treino e inferencia precisam usar a mesma logica de features

#### `src/meu_projeto_ds/models/evaluate.py`

- O que e: modulo de avaliacao.
- Para que serve: calcular metricas e gerar evidencias de qualidade.
- Como usar na pratica: compare candidatos, thresholds, segmentos, erro por grupo, estabilidade.
- Quando e populado: apos treino, antes de promocao.
- Hacks praticos:
  - avalie por slices, nao so metrica global
  - gere saidas legiveis por humanos e maquinas
- O que nunca esquecer:
  - modelo com boa media pode falhar gravemente em segmentos criticos

### Pacote `src/meu_projeto_ds/pipelines/`

#### `src/meu_projeto_ds/pipelines/__init__.py`

- O que e: namespace de orquestracao logica.

#### `src/meu_projeto_ds/pipelines/training.py`

- O que e: definicao logica do pipeline de treino.
- Para que serve: encadear as etapas do treino no codigo.
- Como usar na pratica: chamar ingestao, validacao, features, treino, avaliacao e publicacao.
- Quando e populado: quando voce deixa de rodar modulos manualmente.
- Hacks praticos:
  - diferencie logica do pipeline de agendamento/orquestrador
  - aqui vive o fluxo; em `pipelines/` vive a definicao operacional
- O que nunca esquecer:
  - pipeline claro facilita testes e migracoes entre orquestradores

#### `src/meu_projeto_ds/pipelines/batch_inference.py`

- O que e: definicao logica do pipeline de inferencia em lote.
- Para que serve: orquestrar leitura de input, transformacao, predicao e persistencia.
- Como usar na pratica: ideal para previsoes diarias ou por janela.
- Quando e populado: quando inferencia vira rotina.
- Hacks praticos:
  - trate cada execucao como job auditavel
  - excelente lugar para escrever logs de volume e qualidade
- O que nunca esquecer:
  - inferencia em lote precisa ser repetivel e ter rollback conceitual

### Pacote `src/meu_projeto_ds/monitoring/`

#### `src/meu_projeto_ds/monitoring/__init__.py`

- O que e: namespace de observabilidade de ML.

#### `src/meu_projeto_ds/monitoring/drift.py`

- O que e: modulo para deteccao de drift.
- Para que serve: monitorar mudanca entre dado de treino e dado em producao.
- Como usar na pratica: comparar distribuicoes, ranges, PSI, KL divergence e estatisticas por coluna.
- Quando e populado: idealmente antes ou junto da primeira ida para producao.
- Hacks praticos:
  - comece simples com checks por coluna; nao espere framework robusto
  - drift de input ja entrega muito valor antes de medir drift de performance
- O que nunca esquecer:
  - drift nao e so estatistica; precisa de interpretacao de negocio

### Pacote `src/meu_projeto_ds/utils/`

#### `src/meu_projeto_ds/utils/__init__.py`

- O que e: namespace de utilidades.
- Para que serve: abrigar helpers transversais.

#### `src/meu_projeto_ds/utils/io.py`

- O que e: utilitario de I/O.
- Para que serve: padronizar criacao e manuseio de diretorios e arquivos.
- Como usar na pratica: qualquer etapa que persista output pode usar helpers daqui.
- Quando e populado: cedo, conforme codigo repetido aparece.
- Hacks praticos:
  - so promova para `utils` o que realmente e generico
- O que nunca esquecer:
  - `utils` e a pasta mais facil de virar lixo; seja disciplinado

#### `src/meu_projeto_ds/utils/logging.py`

- O que e: helper de logging.
- Para que serve: centralizar logger e evitar prints espalhados.
- Como usar na pratica: cada modulo chama `get_logger(__name__)`.
- Quando e populado: cedo, assim que pipeline precisa de rastreabilidade.
- Hacks praticos:
  - logging consistente muda muito a depuracao
  - no futuro, inclua correlation id, model version e run id
- O que nunca esquecer:
  - print serve para explorar; logging serve para operar

## Testes

A estrutura de testes e um dos diferenciais entre projeto de estudo e projeto build to learn serio.

### `tests/conftest.py`

- O que e: configuracao compartilhada do pytest.
- Para que serve: neste caso, ajustar o path para o layout `src/`; depois pode ter fixtures comuns.
- Como usar na pratica: concentre fixtures reutilizaveis, factories e setup leve.
- Quando e populado: desde cedo.
- Hacks praticos:
  - use `conftest.py` para reduzir duplicacao
  - otimo lugar para fixtures de datasets sinteticos
- O que nunca esquecer:
  - nao coloque logica pesada demais aqui; senao o teste vira magia

### `tests/unit/`

- O que e: testes unitarios.
- Para que serve: validar pequenas funcoes isoladas.
- Como usar na pratica: teste funcoes puras de features, validacao, config e utilitarios.
- Quando e populado: desde o inicio do codigo.
- Hacks praticos:
  - em ML, unit test e excelente para regras de transformacao e validacao
- O que nunca esquecer:
  - unit test nao prova que o pipeline inteiro funciona

### `tests/unit/test_config.py`

- O que e: teste do modulo de configuracao.
- Para que serve: garantir comportamento minimo esperado de settings.
- Como usar na pratica: expanda para validar defaults, env vars e caminhos.
- Quando e populado: cedo.
- O que nunca esquecer:
  - bugs de configuracao quebram tudo e costumam aparecer tarde

### `tests/integration/`

- O que e: testes de integracao.
- Para que serve: validar a interacao entre modulos.
- Como usar na pratica: treino usando dataset minimo sintetico, pipeline curto, leitura-escrita local.
- Quando e populado: assim que dois ou mais modulos comecam a conversar.
- Hacks praticos:
  - use dados pequenos e deterministicos
  - simule contratos reais com custo baixo
- O que nunca esquecer:
  - integracao nao deve depender de ambiente externo fragil, se puder evitar

### `tests/integration/test_train_module.py`

- O que e: teste simples do modulo de treino.
- Para que serve: garantir que o entrypoint de treino responde como esperado.
- Como usar na pratica: evolua para checar geracao de artefato, metricas e schema do output.
- Quando e populado: quando a primeira rotina de treino aparece.

### `tests/contract/`

- O que e: testes de contrato.
- Para que serve: validar formato e expectativas de interfaces.
- Como usar na pratica: entrada/saida de predicao, schema de features, payload de API e estrutura de artifact.
- Quando e populado: quando seu codigo comeca a ter consumidores claros.
- Hacks praticos:
  - contrato bem testado reduz quebras entre treino, scoring e consumo downstream
- O que nunca esquecer:
  - em ML, quebrar contrato de feature ou predicao e falha operacional seria

### `tests/contract/test_predict_contract.py`

- O que e: teste simples do contrato da inferencia.
- Para que serve: garantir que a saida contem o minimo esperado.
- Como usar na pratica: evolua para checar colunas, tipos, metadados, shape e thresholds.
- Quando e populado: assim que inferencia tiver interface mais estavel.

## Elementos Estruturais Especiais

### `.gitkeep`

- O que e: placeholder vazio.
- Para que serve: manter diretorios no repositorio mesmo vazios.
- Como usar na pratica: so existe para Git; o conteudo real vira depois.
- Quando e populado: no bootstrap.
- Hacks praticos:
  - onde fizer mais sentido pedagogico, substitua por `README.md` curto explicando a pasta
- O que nunca esquecer:
  - `.gitkeep` nao e padrao oficial do Git; e convencao pratica

### `.pytest_cache/`

- O que e: cache gerado pelo pytest.
- Para que serve: acelerar execucoes e armazenar estado do test runner.
- Como usar na pratica: normalmente voce ignora.
- Quando e populado: ao rodar testes.
- Hacks praticos:
  - nenhum grande; deixe ignorado
- O que nunca esquecer:
  - nao trate cache como parte da arquitetura do projeto

## Como essa estrutura se comporta ao longo do pipeline real

Se eu desenhar o ciclo tipico de ponta a ponta:

1. Ingestao
- entra em `data/raw/` e `data/external/`
- logica em `src/meu_projeto_ds/data/ingestion.py`

2. Validacao inicial
- checagens em `src/meu_projeto_ds/data/validation.py`
- output mais limpo em `data/interim/`

3. Transformacao e preparacao
- curadoria vai para `data/processed/`
- engenharia de atributos em `src/meu_projeto_ds/features/engineering.py`
- features podem ser persistidas em `data/features/`

4. Treino
- orquestracao logica em `src/meu_projeto_ds/pipelines/training.py`
- treino em `src/meu_projeto_ds/models/train.py`

5. Avaliacao
- metricas em `src/meu_projeto_ds/models/evaluate.py`
- relatorios em `models/reports/`

6. Serializacao e registro
- binario em `models/serialized/`
- metadata/versao em `models/registry/`

7. Scoring
- logica em `src/meu_projeto_ds/models/predict.py`
- pipeline batch em `src/meu_projeto_ds/pipelines/batch_inference.py`
- definicao operacional em `pipelines/scoring/`

8. Monitoramento
- checks em `src/meu_projeto_ds/monitoring/drift.py`
- jobs operacionais em `pipelines/monitoring/`

9. Qualidade e entrega
- testes em `tests/`
- automacao em `.github/workflows/ci.yml`
- release/empacotamento em `.github/workflows/cd-model.yml`

## Hacks praticos que realmente mudam o jogo

- Promova cedo do notebook para `src/`
  - a maior virada de maturidade em DS acontece quando a logica deixa de viver so em notebook

- Trate dados intermediarios como ativos de debug
  - `data/interim/` bem usado acelera muito troubleshooting

- Faca o treino sempre emitir metadata
  - seed, dataset version, feature version, params, metricas, caminho do artefato

- Padronize contratos de entrada e saida
  - isso prepara o terreno para MLflow, serving, monitoramento e auditoria

- Use dados sinteticos pequenos para testes
  - times de ML travam muito quando teste depende de dataset real pesado

- Diferencie claramente:
  - notebook = descoberta
  - `src/` = logica reusavel
  - `pipelines/` = operacao/agendamento

- Adote a regra:
  - se algo sera executado duas vezes, sai do notebook e vira codigo em `src/`

- Documente decisoes pequenas cedo
  - em projetos de aprendizado, a memoria do porque fizemos assim e tao valiosa quanto o codigo

## O que nunca deve ser esquecido em um projeto CD4ML

- Reprodutibilidade e tao importante quanto acuracia
- Um modelo bom sem rastreabilidade e tecnicamente fragil
- Notebook nao e produto
- Dado bruto deve ser preservado
- Validacao de dados nao e opcional
- Testes em ML nao testam se a IA esta inteligente; testam contratos, transformacao, consistencia e seguranca operacional
- CI de projeto de ML deve ser rapido e confiavel
- Metrica isolada nao basta; precisa de contexto, segmento e evidencia
- Sem monitoramento, o modelo ja comecou a envelhecer
- Estrutura boa nao garante maturidade; disciplina de uso e o que faz a diferenca

## Leitura de mercado: onde essa estrutura ja esta boa e onde ela naturalmente evolui

Ela ja esta boa para:

- aprendizado serio
- baseline profissional
- organizar projeto de DS/ML com testes e CI
- preparar entrada de MLflow
- suportar batch ML com boas praticas

Ela naturalmente evolui para:

- MLflow tracking + model registry
- DVC ou lakehouse para versionamento de dados
- Pandera/Great Expectations para validacao
- Airflow/Kubeflow/Prefect para orquestracao
- monitoramento com metricas operacionais e de drift
- ambientes separados de dev/staging/prod
- promocao formal de modelo por criterios

## Como eu recomendo voce estudar essa estrutura

Sendo build to learn, o melhor caminho e estudar por camadas:

1. Primeiro, entenda profundamente `data/`, `src/` e `tests/`
2. Depois, entenda a separacao entre `src/meu_projeto_ds/pipelines/` e `pipelines/`
3. Em seguida, domine `models/` como evidencia e governanca
4. So entao adicione MLflow, porque ai ele entra em terreno preparado

## Proximos passos sugeridos

1. Fazer um deep dive so em `data/`, com exemplos concretos de ingestao, validacao e versionamento
2. Fazer um deep dive so em `src/`, explicando como transformar notebook em software de ML
3. Fazer um deep dive so em `tests/`, com padrao de mercado para projetos de ML
4. Preparar a base para `MLflow` da forma certa, sem ainda instalar tudo
